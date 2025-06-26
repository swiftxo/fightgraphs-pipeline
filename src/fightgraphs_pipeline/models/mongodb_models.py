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
            'type': 'str',
            'validation_alias': 'ObjectId',
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
    fight_refs: List[str] = []


# --- Fight Models (with nested details) ---

class FightDetailsModel(BaseModel):
    """
    Nested model for the details of a fight's conclusion.
    """
    method: Optional[str]
    round: Optional[str]
    time: Optional[str]
    time_format: Optional[str]
    referee: Optional[str]
    details: Optional[str]


class PerFighterStatsModel(BaseModel):
    """
    Nested model for a single fighter's stats in a bout.
    """
    knockdowns: Optional[str]
    sig_strikes: Optional[str]
    sig_strikes_percent: Optional[str]
    total_strikes: Optional[str]
    takedowns: Optional[str]
    takedowns_percent: Optional[str]
    submission_attempts: Optional[str]
    reversals: Optional[str]
    control_time: Optional[str]


class FightModel(MongoBaseModel):
    """
    Model representing a single fight.
    Corresponds to the 'fights' collection.
    """
    fight_ufcstats_url: Optional[str]
    fighter1_url: Optional[str]
    fighter2_url: Optional[str]
    winner_url: Optional[str]
    loser_url: Optional[str]
    fight_details: Optional[FightDetailsModel]
    fight_stats: Optional[Dict[str, PerFighterStatsModel]] 