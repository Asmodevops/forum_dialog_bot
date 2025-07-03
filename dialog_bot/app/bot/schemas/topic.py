from pydantic import BaseModel


class TopicThreadIdSchema(BaseModel):
    thread_id: int


class TopicUserIdSchema(BaseModel):
    user_id: int
