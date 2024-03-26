from health_check.backends import BaseHealthCheckBackend


class MeldingenTokenCheck(BaseHealthCheckBackend):
    critical_service = False

    def identifier(self):
        return self.__class__.__name__
