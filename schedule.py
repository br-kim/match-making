from typing import List

import crud
import uuid

import models
from dependencies import get_db


def game_matching_1vs1():
    """
    1vs1 매칭
    :return:
    """
    db = next(get_db())
    match_making_info_list = crud.get_match_making_by_game_type(db=db, game_type="1vs1")
    matched_user_id_set = set()
    if len(match_making_info_list) >= 2:
        idx = 0
        while idx < len(match_making_info_list) - 1:
            info1, info2 = match_making_info_list[idx], match_making_info_list[idx + 1]
            room_id = str(uuid.uuid4())
            matching_correction = calculate_1vs1_matching_correction(info1.user)
            if info2.user.mmr - info1.user.mmr < matching_correction:
                for user_id, team in zip([info1.user_id, info2.user_id], ["A", "B"]):
                    crud.update_room_id_by_user_id(
                        db=db,
                        game_type="1vs1",
                        room_id=room_id,
                        user_id=user_id,
                        team=team,
                    )
                print(info1.user_id, info2.user_id, "매칭 성공")
                info1.user.matching_factor.waiting = 0
                info2.user.matching_factor.waiting = 0
                matched_user_id_set.add(info1.user_id)
                matched_user_id_set.add(info2.user_id)
                idx += 1
            idx += 1
    else:
        print("유저 수 부족. 1vs1 매칭 실패")
    for info in match_making_info_list:
        if info.user_id not in matched_user_id_set:
            info.user.matching_factor.waiting += 1
    db.commit()


def game_matching_2vs2():
    """
    2vs2 매칭
    :return:
    """
    db = next(get_db())
    match_making_info_list = crud.get_match_making_by_game_type(db=db, game_type="2vs2")
    matched_user_id_set = set()
    if len(match_making_info_list) >= 4:
        idx = 0
        while idx < len(match_making_info_list) - 3:
            info1, info2 = match_making_info_list[idx], match_making_info_list[idx + 3]
            room_id = str(uuid.uuid4())
            matching_user_list = [
                info.user for info in match_making_info_list[idx : idx + 4]
            ]
            user_id_list = [
                info.user_id for info in match_making_info_list[idx : idx + 4]
            ]
            matching_correction = calculate_2vs2_matching_correction(matching_user_list)
            if info2.user.mmr - info1.user.mmr < matching_correction:
                for user_id, team in zip(user_id_list, ["A", "B", "B", "A"]):
                    crud.update_room_id_by_user_id(
                        db=db,
                        game_type="2vs2",
                        room_id=room_id,
                        user_id=user_id,
                        team=team,
                    )
                print(user_id_list, "매칭 성공")
                for user in matching_user_list:
                    matched_user_id_set.add(user.user_id)
                    user.matching_factor.waiting = 0
                idx += 1
            idx += 1
    else:
        print("유저 수 부족. 2vs2 매칭 실패")
    for info in match_making_info_list:
        if info.user_id not in matched_user_id_set:
            info.user.matching_factor.waiting += 1


def calculate_1vs1_matching_correction(user1: models.User):
    """
    1vs1 매칭 보정 계산 함수
    :param user1:
    :return:
    """
    default_correction = 50
    user1_waiting = min(10, user1.matching_factor.waiting)
    return default_correction + user1_waiting


def calculate_2vs2_matching_correction(users: List[models.User]):
    """
    2vs2 매칭 보정 계산 함수
    :param users:
    :return:
    """
    default_correction = 100
    result = 0
    for user in users:
        result += min(10, user.matching_factor.waiting)
    return default_correction + (result // len(users))
