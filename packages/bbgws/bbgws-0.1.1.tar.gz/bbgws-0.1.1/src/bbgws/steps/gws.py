import os
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from buildbot.db.model import Model
from buildbot.plugins import util
from buildbot.process.buildstep import BuildStep, BuildStepFailed, ShellMixin
from buildbot.process.log import StreamLog
from buildbot.steps.shellsequence import ShellSequence
from buildbot.steps.worker import CompositeStepMixin

from bbgws.event import EventType
from bbgws.steps._stagefilter import Event, Stage, stages_to_run
from bbgws.steps.asyncbuild import AsyncBuildStep


@dataclass
class _After:
    steps: list[BuildStep]
    after_all: bool = False

    def __post_init__(self):
        if not self.steps:
            raise ValueError("after-stage configuration: missing steps")


class GwsStages(ShellMixin, CompositeStepMixin, AsyncBuildStep):
    def __init__(
        self,
        artifacts_root,
        force_flavor: str | None = None,
        and_after: dict | None = None,
        **kwargs,
    ):
        kwargs = self.setupShellMixin(kwargs)
        super().__init__(**kwargs)

        self.artifacts_root = artifacts_root
        self.force_flavor = force_flavor
        self._after: dict[str, _After] = {}

        self._next_steps: list[BuildStep] = []
        self._after_all_steps: list[BuildStep] = []
        self._log: StreamLog | None = None

        if and_after:
            for stage, after_kw in and_after.items():
                self._after[stage] = _After(**after_kw)

    async def arun(self):
        builddir = Path(self.getProperty("builddir"))
        workdir = builddir / self.workdir

        config = await self._load_config(workdir / ".gws.toml")
        if config is None:
            await self.log("Pipeline terminated: .gws.toml not found")
            return util.SUCCESS

        artifacts_root = Path(await self.build.render(self.artifacts_root))
        buildername = self.build.getProperty("buildername") or "unknown-builder"
        buildnumber = self.build.getProperty("buildnumber", -1)
        build_artifacts = artifacts_root / str(buildername) / str(buildnumber)

        self._next_steps.clear()
        self._after_all_steps.clear()

        event = Event(
            EventType(self.build.getProperty("event")),
            self.build.getProperty("ref"),
            self.build.allFiles(),
        )
        to_run = stages_to_run(self._get_stages(config), event)
        if not to_run:
            await self.log(
                f"Pipeline terminated: no matching filter for event: {str(event)}"
            )
            return util.SUCCESS

        self.build.setProperty("artifacts", str(artifacts_root), "Build")
        for stage in to_run:
            if not stage.recipes:
                continue

            if self.force_flavor:
                stage.flavor = self.force_flavor

            # TODO: validate really available flavors against stage.flavor and
            # fail build immediately if it isn't available
            if stage.flavor not in ("ci", "minimal"):
                raise BuildStepFailed(
                    f"flavor not available for '{stage.name}': {stage.flavor}"
                )

            dirname = re.sub(r"\s+", "-", stage.name.lower())
            stage_artifacts = build_artifacts / dirname
            self.build.setProperty(
                f"artifacts.{stage.name}", str(stage_artifacts), "Build"
            )

            self._next_steps.append(await self._justin(stage, workdir, stage_artifacts))
            self._add_after(stage.name)

        self.build.addStepsAfterCurrentStep(self._next_steps + self._after_all_steps)
        return util.SUCCESS

    async def log(self, msg, err=False):
        if self._log is None:
            self._log = await self.addLog("stdio")

        log_fn = self._log.addStderr if err else self._log.addStdout
        await log_fn(msg)

    async def _load_config(self, path: Path):
        gws_toml = await self.getFileContentFromWorker(str(path))

        if not gws_toml:
            return None

        try:
            config = tomllib.loads(gws_toml)
        except tomllib.TOMLDecodeError as e:
            raise BuildStepFailed(f".gws.toml read error: {str(e)}") from e

        self._set_default_config(config)
        return config

    def _get_stages(self, config: dict) -> list[Stage]:
        try:
            return [Stage(**ef) for ef in config["stage"]]
        except (TypeError, ValueError) as e:
            raise BuildStepFailed(f"Invalid [[stage]]: {str(e)}") from e

    def _set_default_config(self, config: dict):
        config.setdefault("stage", [])

    def _add_after(self, stage: str) -> BuildStep:
        if stage not in self._after:
            return

        after = self._after[stage]
        target_list = self._after_all_steps if after.after_all else self._next_steps
        target_list.extend(after.steps)

    async def _justin(self, stage: Stage, workdir: Path, artifacts: Path) -> BuildStep:
        cmd = ["justin", "-F", stage.flavor, "--copy-workspace"]
        cmd += ("--copy-back", f"/artifacts:{artifacts}")
        cmd += ("-e", "CI_WORKSPACE=/workspace")
        cmd += ("-e", "CI_ARTIFACTS=/artifacts")
        cmd += ["justw", "--justfile", str(stage.justfile)]
        cmd.extend(stage.recipes)

        descr = _excerpt(f"Stage: {stage.name or '(default)'}")

        # coerce everything to str, because ShellCommand doesn't take non-str types
        # (like Path) lightly.
        cmd = [str(part) for part in cmd]
        return ShellSequence(
            name=descr,
            workdir=str(workdir),
            haltOnFailure=True,
            commands=[
                util.ShellArg(["mkdir", "-p", str(artifacts.parent)], logname=None),
                util.ShellArg(cmd, logname="Run justin", haltOnFailure=True),
            ],
        )


def _excerpt(s: str) -> str:
    max_name_len = Model.steps.c.name.type.length
    if len(s) > max_name_len:
        ellipsis = "…"
        newlen = max(1, max_name_len - len(ellipsis))
        s = s[:newlen] + ellipsis
    return s
