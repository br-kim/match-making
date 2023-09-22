from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, unique=True)
    mmr = Column(Integer, index=True)
    match_making_info = relationship("MatchMakingInfo", backref="user")


class MatchMakingInfo(Base):
    __tablename__ = "match_making_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.user_id"))
    game_type = Column(String)
    room_id = Column(String)
    ticket = Column(String)
    team = Column(String)


class UserMatchingFactor(Base):
    __tablename__ = "user_matching_factor"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.user_id"))
    waiting = Column(Integer, default=0)
    user = relationship("User", backref="matching_factor")
