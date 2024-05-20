from bbgws.steps.asyncbuild import AsyncBuildStep
from buildbot.plugins import steps, util


# parent class order matters due to MRO (C3 linearization). In a nutshell: we
# want to use AsyncBuildStep.run, not ShellSequence.run.
class CopyArtifacts(AsyncBuildStep, steps.ShellSequence):
    def __init__(self, source, destination, **kwargs):
        if "commands" in kwargs:
            raise ValueError("CopyArtifacts doesn't accept custom commands")

        self.source = source
        self.destination = destination
        super().__init__(**kwargs)

    async def arun(self):
        source = await self.build.render(self.source)
        destination = await self.build.render(self.destination)

        commands = [
            # sanity check - if we didn't set artifacts.pages property for ANY
            # reason, commands would operate on empty strings. For example
            # rsync, which adds a slash after the property, would sync the
            # whole root directory...
            util.ShellArg(["test", "-d", source], haltOnFailure=True, logname="test"),
            # rsync won't create parent directories by itself
            util.ShellArg(["mkdir", "-p", destination], haltOnFailure=True),
            util.ShellArg(
                [
                    "rsync",
                    "--compress",
                    "--recursive",
                    "--dirs",
                    "--links",
                    "--perms",
                    "--times",
                    "--devices",
                    "--specials",
                    "--delete",
                    # note slash at the end
                    f"{source}/",
                    f"{destination}/",
                ],
                logname="rsync",
            ),
            util.ShellArg(["rm", "-r", "-f", source], logname="cleanup"),
        ]

        return await self.runShellSequence(commands)
