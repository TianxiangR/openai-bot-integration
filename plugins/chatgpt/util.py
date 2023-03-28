from nonebot.internal.params import Depends as Depends
from nonebot.adapters import Event


async def _event_user_id(event: Event) -> str:
    return event.get_user_id()


def EventUserId() -> str:
    return Depends(_event_user_id)
