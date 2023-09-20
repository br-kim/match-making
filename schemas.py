from pydantic import BaseModel


class CreateMatchMakingRequest(BaseModel):
    user_id: str
    game_type: str


class CreateUserRequest(BaseModel):
    user_id: str
