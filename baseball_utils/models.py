from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base: Any = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    retro_id = Column(String(25), unique=True)


class Batter(Base):
    __tablename__ = 'batters'


class Pitcher(Base):
    __tablename__ = 'pitchers'


class Umpire(Base):
    __tablename__ = 'umpires'

    id = Column(Integer, primary_key=True)
    retro_id = Column(String(25), unique=True)

    home_games = relationship('Game', back_populates='ump_home')
    first_games = relationship('Game', back_populates='ump_first')
    second_games = relationship('Game', back_populates='ump_second')
    third_games = relationship('Game', back_populates='ump_third')
    left_games = relationship('Game', back_populates='ump_left')
    right_games = relationship('Game', back_populates='ump_right')


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    away_games = relationship('Game', back_populates='visit_team')
    home_games = relationship('Game', back_populates='home_games')


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    visit_team_fk = Column(Integer, ForeignKey('teams.id'))
    home_team_fk = Column(Integer, ForeignKey('teams.id'))
    number = Column(Integer)
    start_dt = Column(DateTime)
    used_dh = Column(Boolean)
    ump_home_fk = Column(Integer, ForeignKey('umpires.id'), nullable=False)
    ump_first_fk = Column(Integer, ForeignKey('umpires.id'), nullable=False)
    ump_second_fk = Column(Integer, ForeignKey('umpires.id'), nullable=False)
    ump_third_fk = Column(Integer, ForeignKey('umpires.id'), nullable=False)
    ump_left_fk = Column(Integer, ForeignKey('umpires.id'))
    ump_right_fk = Column(Integer, ForeignKey('umpires.id'))

    visit_team = relationship('Team', back_populates='away_games')
    home_team = relationship('Team', back_populates='home_games')
    ump_home = relationship('Umpire', back_populates='home_games')
    ump_first = relationship('Umpire', back_populates='first_games')
    ump_second = relationship('Umpire', back_populates='second_games')
    ump_third = relationship('Umpire', back_populates='third_games')
    ump_left = relationship('Umpire', back_populates='left_games')
    ump_right = relationship('Umpire', back_populates='right_games')


class Play(Base):
    __tablename__ = 'plays'

    id = Column(Integer, primary_key=True)
