from common.type_hints import JSONType
from users.models import UserEvent


class UserEventsAnalyzer:
    def __init__(self, params: JSONType):
        self.params = params

    def analyze(self, event: UserEvent) -> None:
        pass
