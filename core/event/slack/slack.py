from core.event.base_event import BaseEvent
from core.event.slack.parameter import SlackEventParameter


class SlackEvent(BaseEvent):
    async def run(self, parameter: SlackEventParameter) -> None:
        print(f"SLACK EVENT / {parameter.channel} / {parameter.message}")
