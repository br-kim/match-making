from pydantic import BaseModel


class CreateMatchMakingRequest(BaseModel):
    user_id: str
    game_type: str
    ticket: str


class CreateUserRequest(BaseModel):
    user_id: str
