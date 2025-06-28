from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Helper class to handle MongoDB ObjectId as a Pydantic type.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core.core_schema import (
            str_schema,
            validation_info,
        )

        return {
            "type": "str",
            "validation_alias": "ObjectId",
        }


class MongoBaseModel(BaseModel):
    """
    Base model for MongoDB documents, including automatic _id and timestamps.
    """


class FighterModel(MongoBaseModel):
    """
    Model representing a fighter's details.
    Corresponds to the 'fighters' collection.
    """

    fighter_ufcstats_url: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    nickname: Optional[str]
    height: Optional[str]
    weight: Optional[str]
    reach: Optional[str]
    stance: Optional[str]
    fighter_record: Optional[str]
    date_of_birth: Optional[str]
    fight_urls: List[str] = []


class FighterImageModel(MongoBaseModel):
    """
    Model for storing a fighter's image URL.
    Corresponds to the 'fighter_images' collection.
    """

    fighter_ufcstats_url: Optional[str]
    fighter_image_url: Optional[str]


class FightRefModel(MongoBaseModel):
    """
    Model representing a fight reference.
    Corresponds to the 'fight_refs' field in the 'events' collection.
    """

    fight_ufcstats_url: Optional[str]
    card_position: Optional[str]


# --- Event Model ---


class EventModel(MongoBaseModel):
    """
    Model representing a fight event.
    Corresponds to the 'events' collection.
    """

    event_name: Optional[str]
    event_date: Optional[str]
    event_location: Optional[str]
    event_status: Optional[str]
    event_ufcstats_url: Optional[str]
    fight_refs: List[FightRefModel]


# --- Fight Models (with nested details) ---


class FightDetailsModel(BaseModel):
    event_ufcstats_url: Optional[str]
    method: Optional[str]
    time: Optional[str]
    time_format: Optional[str]
    referee: Optional[str]
    finish_details: Optional[str]
    fight_of_the_night: Optional[str]
    performance_of_the_night: Optional[str]
    weight_class: Optional[str]
    title_fight: Optional[str]
    judge1_name: Optional[str]
    judge1_score: Optional[str]
    judge2_name: Optional[str]
    judge2_score: Optional[str]
    judge3_name: Optional[str]
    judge3_score: Optional[str]


class PerFighterRoundStatsModel(BaseModel):
    """
    Nested model for a fighter's stats in a round of a fight.
    """

    kd: Optional[str]
    fighter_ufcstats_url: Optional[str]
    sig_strikes: Optional[str]
    total_strikes: Optional[str]
    takedowns: Optional[str]
    sub_attempts: Optional[str]
    reversals: Optional[str]
    control_time: Optional[str]
    head_strikes: Optional[str]
    body_strikes: Optional[str]
    leg_strikes: Optional[str]
    distance_strikes: Optional[str]
    clinch_strikes: Optional[str]
    ground_strikes: Optional[str]


class RoundStatsModel(BaseModel):
    fighter1: PerFighterRoundStatsModel
    fighter2: PerFighterRoundStatsModel


class FighterInfoModel(BaseModel):
    name: Optional[str]
    fighter_ufcstats_url: Optional[str]
    fighter_status: Optional[str]


class FightModel(MongoBaseModel):
    """
    Model representing a single fight.
    Corresponds to the 'fights' collection.
    """

    fight_ufcstats_url: Optional[str]
    fighter1: FighterInfoModel
    fighter2: FighterInfoModel
    fight_details: Optional[FightDetailsModel]
    fight_stats: Optional[Dict[str, RoundStatsModel]]
