class SchafkopfError(Exception):
    pass


class RoundLevelError(SchafkopfError):
    def __init__(self, message):
        self.message = message


class GameLevelError(SchafkopfError):
    def __init__(self, message):
        self.message = message