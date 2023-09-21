import crud
import uuid
from dependencies import get_db


def game_matching_1vs1():
    db = next(get_db())
    match_making_info_list = crud.get_match_making_by_game_type(db=db, game_type="1vs1")
    if len(match_making_info_list) > 1:
        idx = 0
        while idx < len(match_making_info_list) - 1:
            print(idx, str(uuid.uuid4()))
            info1, info2 = match_making_info_list[idx], match_making_info_list[idx + 1]
            room_id = str(uuid.uuid4())
            if info2.user.mmr - info1.user.mmr < 50:
                crud.update_room_id_by_user_ids(
                    db=db,
                    game_type="1vs1",
                    room_id=room_id,
                    user_ids=[info1.user_id, info2.user_id],
                )
                print(info1.user_id, info2.user_id, "매칭 성공")
                idx += 1
            idx += 1
    else:
        print("유저 수 부족으로 1vs1 매칭 실패")
