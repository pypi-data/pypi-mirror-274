from buildbot.process.buildstep import BuildStep
from twisted.internet.defer import Deferred

class AsyncBuildStep(BuildStep):
    def run(self):
        return Deferred.fromCoroutine(self.arun())
