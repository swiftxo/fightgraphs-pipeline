from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    Boolean,
    ForeignKey,
    Time,
    Text,
)
from sqlalchemy.orm import relationship, declarative_base

# Define the declarative base
Base = declarative_base()

def get_postgres_base() -> Base:
    """
    Returns the declarative base for PostgreSQL models.
    This function is used to ensure that the Base is correctly initialized
    and can be used to create models.
    """
    return Base

class PromotionEntity(Base):
    """SQLAlchemy model for the promotion table."""
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)

    # Relationships
    events = relationship("EventEntity", back_populates="promotion")
    weightclasses = relationship("WeightclassEntity", back_populates="promotion")


class EventEntity(Base):
    """SQLAlchemy model for the event table."""
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(100), nullable=False)
    ufcstats_url = Column(String(255), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotion.id"), nullable=False)

    # Relationships
    promotion = relationship("PromotionEntity", back_populates="events")
    fights = relationship("FightEntity", back_populates="event")


class WeightclassEntity(Base):
    """SQLAlchemy model for the weightclass table."""
    __tablename__ = "weightclass"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    min_weight_kg = Column(Numeric(5, 2))
    max_weight_kg = Column(Numeric(5, 2))
    gender = Column(String(10), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotion.id"), nullable=False)

    # Relationships
    promotion = relationship("PromotionEntity", back_populates="weightclasses")
    titles = relationship("TitleEntity", back_populates="weightclass")
    fights = relationship("FightEntity", back_populates="weight_class")


class TitleEntity(Base):
    """SQLAlchemy model for the title table."""
    __tablename__ = "title"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    title_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False)
    weightclass_id = Column(Integer, ForeignKey("weightclass.id"))

    # Relationships
    weightclass = relationship("WeightclassEntity", back_populates="titles")
    title_fights = relationship("TitleFightEntity", back_populates="title")


class FighterEntity(Base):
    """SQLAlchemy model for the fighter table."""
    __tablename__ = "fighter"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    nickname = Column(String(100))
    date_of_birth = Column(Date)
    height_cm = Column(Numeric(5, 2))
    weight_kg = Column(Numeric(5, 2))
    reach_cm = Column(Numeric(5, 2))
    stance = Column(String(50), nullable=False)
    image_url = Column(String(255))
    ufcstats_url = Column(String(255), nullable=False)

    # Relationships for fights
    fights1 = relationship("FightEntity", foreign_keys="[FightEntity.fighter1_id]", back_populates="fighter1")
    fights2 = relationship("FightEntity", foreign_keys="[FightEntity.fighter2_id]", back_populates="fighter2")
    wins = relationship("FightEntity", foreign_keys="[FightEntity.winner_id]", back_populates="winner")

    # Other relationships
    fight_stats = relationship("FightStatEntity", back_populates="fighter")
    fight_bonuses = relationship("FightBonusEntity", back_populates="fighter")
    scorecards = relationship("ScorecardEntity", back_populates="fighter")
    fighter_record = relationship("FighterRecordEntity", back_populates="fighter", uselist=False)


class TimeFormatEntity(Base):
    """SQLAlchemy model for the timeformat table."""
    __tablename__ = "timeformat"

    id = Column(Integer, primary_key=True, nullable=False)
    format_string = Column(Text, nullable=False, unique=True)
    base_rounds = Column(Integer)
    base_round_duration = Column(Integer, nullable=False)
    overtime_rounds = Column(Integer, default=0)
    overtime_duration = Column(Integer)
    unlimited_rounds = Column(Boolean, default=False)
    no_time_limit = Column(Boolean, default=False)

    # Relationship
    fights = relationship("FightEntity", back_populates="time_format")


class RefereeEntity(Base):
    """SQLAlchemy model for the referee table."""
    __tablename__ = "referee"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)

    # Relationship
    fights = relationship("FightEntity", back_populates="referee")


class FightEntity(Base):
    """SQLAlchemy model for the fight table."""
    __tablename__ = "fight"

    id = Column(Integer, primary_key=True, nullable=False)
    method = Column(String(50))
    finish_details = Column(String(255))
    time_format_id = Column(Integer, ForeignKey("timeformat.id"), nullable=False)
    round_finished = Column(Integer)
    time_finished = Column(Time)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    fighter1_id = Column(Integer, ForeignKey("fighter.id"), nullable=False)
    fighter2_id = Column(Integer, ForeignKey("fighter.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("fighter.id"))
    weight_class_id = Column(Integer, ForeignKey("weightclass.id"), nullable=False)
    referee_id = Column(Integer, ForeignKey("referee.id"))
    ufcstats_url = Column(String(255), nullable=False)

    # Relationships
    event = relationship("EventEntity", back_populates="fights")
    time_format = relationship("TimeFormatEntity", back_populates="fights")
    referee = relationship("RefereeEntity", back_populates="fights")
    weight_class = relationship("WeightclassEntity", back_populates="fights")

    fighter1 = relationship("FighterEntity", foreign_keys=[fighter1_id], back_populates="fights1")
    fighter2 = relationship("FighterEntity", foreign_keys=[fighter2_id], back_populates="fights2")
    winner = relationship("FighterEntity", foreign_keys=[winner_id], back_populates="wins")

    title_fights = relationship("TitleFightEntity", back_populates="fight")
    fight_stats = relationship("FightStatEntity", back_populates="fight")
    fight_bonuses = relationship("FightBonusEntity", back_populates="fight")
    scorecards = relationship("ScorecardEntity", back_populates="fight")


class TitleFightEntity(Base):
    """SQLAlchemy model for the titlefight table."""
    __tablename__ = "titlefight"

    id = Column(Integer, primary_key=True, nullable=False)
    fight_id = Column(Integer, ForeignKey("fight.id"), nullable=False)
    title_id = Column(Integer, ForeignKey("title.id"), nullable=False)

    # Relationships
    fight = relationship("FightEntity", back_populates="title_fights")
    title = relationship("TitleEntity", back_populates="title_fights")


class FightStatEntity(Base):
    """SQLAlchemy model for the fightstat table."""
    __tablename__ = "fightstat"

    id = Column(Integer, primary_key=True, nullable=False)
    round = Column(Integer, nullable=False)
    significant_strikes_attempted = Column(Integer, default=0)
    significant_strikes_landed = Column(Integer, default=0)
    total_strikes_landed = Column(Integer, default=0)
    total_strikes_attempted = Column(Integer, default=0)
    knockdowns = Column(Integer, default=0)
    takedowns_landed = Column(Integer, default=0)
    takedowns_attempted = Column(Integer, default=0)
    submissions_attempted = Column(Integer, default=0)
    reversals = Column(Integer, default=0)
    control_time_seconds = Column(Integer, default=0)
    head_strikes_landed = Column(Integer, default=0)
    head_strikes_attempted = Column(Integer, default=0)
    body_strikes_landed = Column(Integer, default=0)
    body_strikes_attempted = Column(Integer, default=0)
    leg_strikes_landed = Column(Integer, default=0)
    leg_strikes_attempted = Column(Integer, default=0)
    ground_strikes_landed = Column(Integer, default=0)
    ground_strikes_attempted = Column(Integer, default=0)
    clinch_strikes_landed = Column(Integer, default=0)
    clinch_strikes_attempted = Column(Integer, default=0)
    distance_strikes_landed = Column(Integer, default=0)
    distance_strikes_attempted = Column(Integer, default=0)
    fighter_id = Column(Integer, ForeignKey("fighter.id"), nullable=False)
    fight_id = Column(Integer, ForeignKey("fight.id"), nullable=False)

    # Relationships
    fighter = relationship("FighterEntity", back_populates="fight_stats")
    fight = relationship("FightEntity", back_populates="fight_stats")


class BonusEntity(Base):
    """SQLAlchemy model for the bonus table."""
    __tablename__ = "bonus"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)

    # Relationship
    fight_bonuses = relationship("FightBonusEntity", back_populates="bonus")


class FightBonusEntity(Base):
    """SQLAlchemy model for the fightbonus table."""
    __tablename__ = "fightbonus"

    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    fight_id = Column(Integer, ForeignKey("fight.id"), nullable=False)
    fighter_id = Column(Integer, ForeignKey("fighter.id"), nullable=False)
    bonus_id = Column(Integer, ForeignKey("bonus.id"), nullable=False)

    # Relationships
    fight = relationship("FightEntity", back_populates="fight_bonuses")
    fighter = relationship("FighterEntity", back_populates="fight_bonuses")
    bonus = relationship("BonusEntity", back_populates="fight_bonuses")


class JudgeEntity(Base):
    """SQLAlchemy model for the judge table."""
    __tablename__ = "judge"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)

    # Relationship
    scorecards = relationship("ScorecardEntity", back_populates="judge")


class ScorecardEntity(Base):
    """SQLAlchemy model for the scorecard table."""
    __tablename__ = "scorecard"

    id = Column(Integer, primary_key=True, nullable=False)
    fight_id = Column(Integer, ForeignKey("fight.id"), nullable=False)
    judge_id = Column(Integer, ForeignKey("judge.id"), nullable=False)
    fighter_id = Column(Integer, ForeignKey("fighter.id"), nullable=False)
    scorecard = Column(Integer, nullable=False)

    # Relationships
    fight = relationship("FightEntity", back_populates="scorecards")
    judge = relationship("JudgeEntity", back_populates="scorecards")
    fighter = relationship("FighterEntity", back_populates="scorecards")


class FighterRecordEntity(Base):
    """SQLAlchemy model for the fighterrecord table."""
    __tablename__ = "fighterrecord"

    id = Column(Integer, primary_key=True, nullable=False)
    fighter_id = Column(Integer, ForeignKey("fighter.id"), nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    no_contests = Column(Integer, default=0)

    # Relationship
    fighter = relationship("FighterEntity", back_populates="fighter_record")

