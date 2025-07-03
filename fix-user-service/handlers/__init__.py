from faststream.nats import NatsRouter

from . import user_fixation


def get_routers() -> list[NatsRouter]:
    return [user_fixation.router]
