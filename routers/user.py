from fastapi import APIRouter, Depends

import crud
from dependencies import get_db
from schemas import CreateUserRequest

user_router = APIRouter()


@user_router.post("/user")
async def post_user(request_body: CreateUserRequest, db=Depends(get_db)):
    """
    유저 생성 API (사용처 없음)
    :param request_body:
    :param db:
    :return:
    """
    user = crud.create_user(db=db, user_id=request_body.user_id)
