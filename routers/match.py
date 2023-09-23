from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates

import crud
from dependencies import get_db
from schemas import CreateMatchMakingRequest

match_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@match_router.post("/match/register")
async def post_match_making(request_body: CreateMatchMakingRequest, db=Depends(get_db)):
    """
    매칭 등록 API
    :param request_body:
    :param db:
    :return:
    """
    user = crud.get_user_by_user_id(db=db, user_id=request_body.user_id)
    if not user:
        user = crud.create_user(db=db, user_id=request_body.user_id)
    match_making = crud.create_match_making(
        db=db,
        user_id=user.user_id,
        game_type=request_body.game_type,
        ticket=request_body.ticket,
    )


@match_router.delete("/match")
async def delete_match_making(user_id: str, db=Depends(get_db)):
    """
    아직 매칭 되지 않은 매칭 대기 삭제 API
    :param user_id:
    :param db:
    :return:
    """
    crud.delete_match_making(db, user_id)


@match_router.get("/match/result")
async def get_match_making_result(ticket: str, db=Depends(get_db)):
    """
    매칭 결과 조회 API
    :param ticket:
    :param db:
    :return:
    """
    match_making = crud.get_match_making(db=db, ticket=ticket)
    if match_making:
        if match_making.room_id:
            return {"room_id": match_making.room_id}
    return {"room_id": None}
