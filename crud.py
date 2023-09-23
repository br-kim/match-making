from sqlalchemy.orm import Session

import models


def get_user_by_user_id(db: Session, user_id):
    """
    user_id로 유저 조회
    :param db:
    :param user_id:
    :return:
    """
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user


def create_user(db: Session, user_id):
    """
    유저 생성 및 유저의 matching factor 생성
    :param db:
    :param user_id:
    :return:
    """
    user = models.User(user_id=user_id, mmr=1000)
    matching_factor = models.UserMatchingFactor(user_id=user_id)
    db.add(user)
    db.add(matching_factor)
    db.commit()
    return user


def create_match_making(db: Session, user_id, game_type, ticket):
    """
    매칭 요청 생성
    :param db:
    :param user_id:
    :param game_type:
    :param ticket:
    :return:
    """
    match_making_info = models.MatchMakingInfo(
        user_id=user_id, game_type=game_type, ticket=ticket
    )
    db.add(match_making_info)
    user_match_making_factor = (
        db.query(models.UserMatchingFactor)
        .filter(models.UserMatchingFactor.user_id == user_id)
        .first()
    )
    user_match_making_factor.waiting = 0
    db.commit()
    return match_making_info


def delete_match_making(db: Session, user_id):
    """
    아직 room id가 배정되지 않은 매칭 삭제
    :param db:
    :param user_id:
    :return:
    """
    db.query(models.MatchMakingInfo).filter(
        models.MatchMakingInfo.user_id == user_id,
        models.MatchMakingInfo.room_id.is_(None),
    ).delete()
    db.commit()


def get_match_making(db: Session, ticket) -> models.MatchMakingInfo | None:
    """
    ticket으로 매칭 조회
    :param db:
    :param ticket:
    :return:
    """
    match_making_info = (
        db.query(models.MatchMakingInfo)
        .filter(models.MatchMakingInfo.ticket == ticket)
        .first()
    )
    return match_making_info


def get_match_making_by_game_type(db: Session, game_type):
    """
    game type별 대기중인 매칭 조회
    :param db:
    :param game_type:
    :return:
    """
    result = (
        db.query(models.MatchMakingInfo)
        .join(models.User)
        .filter(
            models.MatchMakingInfo.game_type == game_type,
            models.MatchMakingInfo.room_id.is_(None),
        )
        .order_by(models.User.mmr.asc())
        .all()
    )

    return result


def update_room_id_by_user_id(db: Session, room_id, user_id, game_type, team):
    """
    매칭 요청에 room_id 및 팀 업데이트
    :param db:
    :param room_id:
    :param user_id:
    :param game_type:
    :param team:
    :return:
    """
    match_making_info = (
        db.query(models.MatchMakingInfo)
        .filter(
            models.MatchMakingInfo.user_id == user_id,
            models.MatchMakingInfo.game_type == game_type,
            models.MatchMakingInfo.room_id.is_(None),
        )
        .update({"room_id": room_id, "team": team})
    )
    db.commit()
