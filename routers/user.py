from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

import crud
from dependencies import get_db
from schemas import CreateMatchMakingRequest, CreateUserRequest

user_router = APIRouter()


@user_router.post("/user")
async def post_user(request_body: CreateUserRequest, db=Depends(get_db)):
    user = crud.create_user(db=db, user_id=request_body.user_id)
