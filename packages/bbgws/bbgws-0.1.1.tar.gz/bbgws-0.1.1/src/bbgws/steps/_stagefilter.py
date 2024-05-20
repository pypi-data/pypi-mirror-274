from dataclasses import dataclass, field
from enum import Enum
from fnmatch import fnmatch, fnmatchcase
from pathlib import Path
from typing import List, Tuple

from bbgws.event import EventType


class PatternType(Enum):
    Negative = False
    Positive = True


@dataclass
class StageOn:
    # filters set to None are disabled (will always match)
    event: EventType | None = None
    tags: List[str] | None = None
    branches: List[str] | None = None
    files_ignore: List[str] | None = None
    files: List[str] | None = None

    def __post_init__(self):
        # technically these filters should be lists, but people make mistakes,
        # so let's correct them.
        for name in ("tags", "branches", "files", "files_ignore"):
            val = getattr(self, name)
            if isinstance(val, str):
                setattr(self, name, [val])

        if isinstance(self.event, str):
            self.event = EventType(self.event)

        if name == "":
            raise ValueError("empty name of stage")


@dataclass
class Stage:
    name: str
    recipes: List[str]
    justfile: Path = Path("justfile")
    flavor: str = "ci"
    on: StageOn | None = None

    def __post_init__(self):
        if isinstance(self.recipes, str):
            self.recipes = [self.recipes]
        if isinstance(self.justfile, str):
            self.justfile = Path(self.justfile)

        if isinstance(self.on, dict):
            self.on = StageOn(**self.on)
        if self.on is not None and not isinstance(self.on, StageOn):
            raise ValueError(f"stage.on for {self.name} is not a table")


@dataclass
class Event:
    event_type: EventType
    changed_ref: str | None = None
    files: List[str] | None = None


@dataclass
class Verdict:
    _verdict: bool = field(default=True, init=False)

    def update(self, fn, *args, **kwargs):
        if self._verdict is False:
            return False

        self._verdict &= fn(*args, **kwargs)
        return self._verdict

    def set_false(self):
        self._verdict = False

    @property
    def verdict(self) -> bool:
        return self._verdict


def stages_to_run(stages: list[Stage], event: Event) -> list[Stage]:
    return [stage for stage in stages if _event_matches(stage, event)]


def _event_matches(stage: Stage, event: Event) -> bool:
    verdict = Verdict()

    if stage.on:
        verdict.update(_event_matcher, stage.on, event)
        verdict.update(_ref_matcher, stage.on, event)
        verdict.update(_files_ignore_matcher, stage.on, event)
        verdict.update(_files_matcher, stage.on, event)

    return verdict.verdict


def _is_tag(event: Event):
    return event.changed_ref and event.changed_ref.startswith("refs/tags/")


def _event_matcher(on: StageOn, event: Event):
    return on.event is None or on.event is event.event_type


def _ref_matcher(on: StageOn, event: Event):
    if on.tags is None and on.branches is None:
        return True
    if not event.changed_ref:
        return False

    def pat(prefix: str, pattern: str):
        if pattern.startswith("!"):
            return f"!{prefix}{pattern[1:]}"
        return f"{prefix}{pattern}"

    tag_refs = [pat("refs/tags/", t) for t in (on.tags or [])]
    branch_refs = [pat("refs/heads/", b) for b in (on.branches or [])]
    return _match_with_exclusions(event.changed_ref, tag_refs + branch_refs)


def _get_pattern_types(patterns: List[str]) -> Tuple[bool, bool]:
    any_positive = False
    any_negative = False
    for pattern in patterns:
        if pattern.startswith("!"):
            any_negative = True
        else:
            any_positive = True
        if any_positive and any_negative:
            break

    return any_positive, any_negative


def _files_ignore_matcher(on: StageOn, event: Event):
    # returning true here means that we're de-facto disabling this check for
    # some types of events or configurations
    if event.event_type != EventType.Push:
        return True
    if on.files_ignore is None:
        return True
    if _is_tag(event):
        return True

    if not event.files:
        return False

    # if at least 1 file doesn't match, then stage should start; in other
    # words: if all files match, then stage should not start
    return not _match_all_of_with_exclusions(
        event.files, on.files_ignore, normcase=False
    )


def _files_matcher(on: StageOn, event: Event):
    # returning true here means that we're de-facto disabling this check for
    # some types of events or configurations
    if event.event_type != EventType.Push:
        return True
    if on.files is None:
        return True
    if _is_tag(event):
        return True

    if not event.files:
        return False

    return _match_any_of_with_exclusions(event.files, on.files)


def _pattern_match(name: str, pattern: str, normcase=True) -> Tuple[PatternType, bool]:
    fnm = fnmatchcase if normcase else fnmatch
    if pattern.startswith("!"):
        return PatternType.Negative, fnm(name, pattern[1:])
    return PatternType.Positive, fnm(name, pattern)


def _match_with_exclusions(name: str, patterns: List[str], normcase=True) -> bool:
    result = False
    for pattern in patterns:
        pt, pr = _pattern_match(name, pattern, normcase)
        if pt is PatternType.Positive:
            result |= pr
        elif pt is PatternType.Negative and pr is True:
            result = False
    return result


def _match_any_of_with_exclusions(
    names: List[str], patterns: List[str], normcase=True
) -> bool:
    return any(_match_with_exclusions(name, patterns, normcase) for name in names)


def _match_all_of_with_exclusions(
    names: List[str], patterns: List[str], normcase=True
) -> bool:
    return all(_match_with_exclusions(name, patterns, normcase) for name in names)
