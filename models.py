from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    mmr = Column(Integer, index=True)


class MatchMakingInfo(Base):
    __tablename__ = "match_making_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    game_type = Column(String)
    room_id = Column(String)