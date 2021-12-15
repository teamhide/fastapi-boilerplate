class InvalidEventTypeException(Exception):
    def __init__(self):
        super().__init__("event must inherit BaseEvent")


class InvalidParameterTypeException(Exception):
    def __init__(self):
        super().__init__("parameter must inherit BaseModel")
