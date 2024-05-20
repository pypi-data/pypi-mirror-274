import fnmatch
import hmac
import json

from buildbot.util import bytes2unicode
from buildbot.www.hooks.base import BaseHookHandler
from dateutil.parser import parse as dateparse
from twisted.python import log

from bbgws.event import EventType


class Missing:
    pass


MISSING = Missing()


def get_field(d, fields, default=MISSING):
    """Gets json path, which can be specified as "key1.key2.key3"""
    for field in fields.split("."):
        try:
            d = d[field]
        except KeyError as e:
            if default is MISSING:
                raise ValueError(f"Invalid JSON: {fields} missing") from e
            return default

    return d


def verify_signature(key: str | None, payload: bytes, signature: str | None) -> bool:
    if signature is None or key is None:
        return False

    calculated = hmac.new(key=key.encode(), msg=payload, digestmod="sha256").hexdigest()
    return hmac.compare_digest(calculated, signature)


def verify_payload(payload, options):
    def verify_option_patterns(value, optname):
        # This also handles EMPTY list. If user sets option to empty list, it will always
        # disallow request.
        opt = options.get(optname, None)
        if opt is not None and not any(
            fnmatch.fnmatch(value, pattern) for pattern in opt
        ):
            raise ValueError(f"'{value}' disallowed by {optname}")

    def verify_ref(value):
        ref_parts = [rp.strip() for rp in value.split("/")]
        if len(ref_parts) != 3 or ref_parts[0] != "refs":
            raise ValueError(f"Not a ref: {value}")

        if not all(ref_parts):  # check that all strings convert to bool - are not empty
            raise ValueError(f"Invalid a ref: '{value}'")

    verify_option_patterns(
        get_field(payload, "repository.clone_url"), "allowed_clone_urls"
    )
    verify_option_patterns(get_field(payload, "pusher.username"), "allowed_pushers")
    verify_ref(get_field(payload, "ref"))


def validate_headers(request):
    content_type = bytes2unicode(request.getHeader(b"Content-Type"))
    if content_type != "application/json":
        raise ValueError(f"Unsupported content-type: {content_type}")

    event = bytes2unicode(request.getHeader(b"X-Gitea-Event-Type"))
    try:
        EventType(event)
    except ValueError as e:
        raise ValueError(f"Unsupported event: {event}") from e


def get_files(commit) -> list[str] | None:
    files = set()

    field = get_field(commit, "files", {})
    for changetype in ("added", "modified", "removed"):
        files.update(field.get(changetype, []))

    return sorted(files)


class GWSHandler(BaseHookHandler):
    def __init__(self, master, options=None):
        if options is None:
            options = {}
        super().__init__(master, options)

        # let's store all available options here for a reference
        self.secret = self.options.get("secret", None)
        self.postprocess = self.options.get("postprocess", None)
        self.allowed_pushers = self.options.get("allowed_pushers", None)
        self.allowed_clone_urls = self.options.get("allowed_clone_urls", None)

    def getChanges(self, request):
        contentb = request.content.read()

        signature = bytes2unicode(request.getHeader(b"X-Gitea-Signature"))
        if not verify_signature(self.secret, contentb, signature):
            if self.secret is None:
                log.msg(
                    "secret not set for gws webhook; rejecting all incoming requests"
                )
            raise ValueError("Not authenticated")

        validate_headers(request)

        payload = json.loads(bytes2unicode(contentb))
        verify_payload(payload, self.options)

        # ignore refs which are not tags or ordinary branches
        ref_parts = get_field(payload, "ref").split("/")
        if ref_parts[1] not in ("tags", "heads"):
            return []

        # common parts
        refname = ref_parts[2]
        repository_url = get_field(payload, "repository.clone_url")
        name = get_field(payload, "repository.full_name")
        full_name = get_field(payload, "repository.full_name")
        html_url = get_field(payload, "repository.html_url", default=None)
        event = bytes2unicode(request.getHeader(b"X-Gitea-Event-Type"))

        changes = []
        for commit in get_field(payload, "commits"):
            author = get_field(commit, "author.name")
            email = get_field(commit, "author.email")
            revision = get_field(commit, "id")

            change = {
                "author": f"{author} <{email}>",
                "files": get_files(commit),
                "comments": get_field(commit, "message"),
                "revision": revision,
                "when_timestamp": dateparse(get_field(commit, "timestamp")),
                "branch": refname,
                "repository": repository_url,
                "project": full_name,
                "category": event,
                "properties": {
                    "event": event,
                    "name": name,
                    "ref": get_field(payload, "ref"),
                    "is_tag": ref_parts[1] == "tags",
                    "is_branch": ref_parts[1] == "heads",
                },
            }
            if html_url:
                change["revlink"] = f"{html_url}/commit/?id={revision}"

            changes.append(change)

        if self.postprocess:
            changes = self.postprocess(request, changes)

        return (changes, "git")


gws = GWSHandler
