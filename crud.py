from sqlalchemy.orm import Session

import models


def get_user_by_user_id(db: Session, user_id):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user


def create_user(db: Session, user_id):
    user = models.User(user_id=user_id, mmr=1000)
    db.add(user)
    db.commit()
    return user


def create_match_making(db: Session, user_id, game_type, ticket):
    match_making_info = models.MatchMakingInfo(
        user_id=user_id, game_type=game_type, ticket=ticket
    )
    db.add(match_making_info)
    db.commit()
    return match_making_info


def delete_match_making(db: Session, user_id):
    db.query(models.MatchMakingInfo).filter(
        models.MatchMakingInfo.user_id == user_id
    ).delete()
    db.commit()


def get_match_making(db: Session, ticket) -> models.MatchMakingInfo | None:
    match_making_info = (
        db.query(models.MatchMakingInfo)
        .filter(models.MatchMakingInfo.ticket == ticket)
        .first()
    )
    return match_making_info


def get_match_making_by_game_type(db: Session, game_type):
    result = (
        db.query(models.MatchMakingInfo)
        .filter(
            models.MatchMakingInfo.game_type == game_type,
            models.MatchMakingInfo.room_id.is_(None),
        )
        .all()
    )
    return result


def update_room_id_by_user_ids(db: Session, room_id, user_ids, game_type):
    match_making_info = (
        db.query(models.MatchMakingInfo)
        .filter(
            models.MatchMakingInfo.user_id.in_(user_ids),
            models.MatchMakingInfo.game_type == game_type,
            models.MatchMakingInfo.room_id.is_(None),
        )
        .update({"room_id": room_id})
    )
    db.commit()
