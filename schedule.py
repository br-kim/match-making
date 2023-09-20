import crud
import uuid
from dependencies import get_db


def game_matching_1vs1():
    db = next(get_db())
    matching_users = crud.get_match_making_by_game_type(db=db, game_type="1vs1")
    if len(matching_users) > 1:
        user1, user2 = matching_users[0], matching_users[1]
        crud.update_room_id_by_user_ids(
            db=db,
            game_type="1vs1",
            room_id=str(uuid.uuid4()),
            user_ids=[user.user_id for user in [user1, user2]],
        )
        print(user1.user_id, user2.user_id, "matched 1vs1 game")
    else:
        print("유저 수 부족으로 1vs1 매칭 실패")
