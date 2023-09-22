import crud
import uuid
from dependencies import get_db


def game_matching_1vs1():
    db = next(get_db())
    match_making_info_list = crud.get_match_making_by_game_type(db=db, game_type="1vs1")
    if len(match_making_info_list) >= 2:
        idx = 0
        while idx < len(match_making_info_list) - 1:
            print(idx, str(uuid.uuid4()))
            info1, info2 = match_making_info_list[idx], match_making_info_list[idx + 1]
            room_id = str(uuid.uuid4())
            if info2.user.mmr - info1.user.mmr < 50:
                for user_id, team in zip([info1.user_id, info2.user_id], ["A", "B"]):
                    crud.update_room_id_by_user_id(
                        db=db,
                        game_type="1vs1",
                        room_id=room_id,
                        user_id=user_id,
                        team=team,
                    )
                print(info1.user_id, info2.user_id, "매칭 성공")
                idx += 1
            idx += 1
    else:
        print("유저 수 부족. 1vs1 매칭 실패")


def game_matching_2vs2():
    db = next(get_db())
    match_making_info_list = crud.get_match_making_by_game_type(db=db, game_type="2vs2")
    if len(match_making_info_list) >= 4:
        idx = 0
        while idx < len(match_making_info_list) - 3:
            info1, info2 = match_making_info_list[idx], match_making_info_list[idx + 3]
            room_id = str(uuid.uuid4())
            user_id_list = [
                info.user_id for info in match_making_info_list[idx : idx + 4]
            ]
            if info2.user.mmr - info1.user.mmr < 100:
                for user_id, team in zip(user_id_list, ["A", "B", "B", "A"]):
                    crud.update_room_id_by_user_id(
                        db=db,
                        game_type="2vs2",
                        room_id=room_id,
                        user_id=user_id,
                        team=team,
                    )
                print(user_id_list, "매칭 성공")
                idx += 1
            idx += 1
    else:
        print("유저 수 부족. 2vs2 매칭 실패")
