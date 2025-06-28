from fightgraphs_pipeline.models.mongodb_models import (
    FighterInfoModel,
    FighterModel,
    EventModel,
    FighterImageModel,
    FightDetailsModel,
    PerFighterRoundStatsModel,
    RoundStatsModel,
    FightModel,
    FightRefModel,
)

from fightgraphs_pipeline.database.mongodb_controller import MongoDBController


def extract_fighters(
    controller: MongoDBController, collection_name: str = "fighters"
) -> list[FighterModel]:
    """
    Extracts fighters from a MongoDB collection.

    Args:
        collection_name (str): The name of the collection to extract fighters from.
        controller (MongoDBController): An instance of the MongoDBController class.

    Returns:
        list[FighterModel]: A list of FighterModel objects representing the extracted fighters.
    """
    fighters_collection = controller.get_collection(collection_name)
    fighters = [FighterModel(**fighter) for fighter in fighters_collection.find()]
    return fighters


def extract_fighter_images(
    controller: MongoDBController, collection_name: str = "fighter_images"
) -> list[FighterImageModel]:
    """
    Extracts fighter images from a MongoDB collection.

    Args:
        collection_name (str): The name of the collection to extract fighter images from.
        controller (MongoDBController): An instance of the MongoDBController class.

    Returns:
        list[FighterImageModel]: A list of FighterImageModel objects representing the extracted fighter images.
    """
    fighter_images_collection = controller.get_collection(collection_name)
    fighter_images = [
        FighterImageModel(**fighter_image)
        for fighter_image in fighter_images_collection.find()
    ]
    return fighter_images


def extract_events(
    controller: MongoDBController, collection_name: str = "events"
) -> list[EventModel]:
    """
    Extracts events from a MongoDB collection.

    Args:
        collection_name (str): The name of the collection to extract events from.
        controller (MongoDBController): An instance of the MongoDBController class.

    Returns:
        list[EventModel]: A list of EventModel objects representing the extracted events.
    """
    events = []
    events_collection = controller.get_collection(collection_name)
    for event in events_collection.find():
        fight_refs = [
            FightRefModel(fight_ufcstats_url=url, card_position=pos)
            for url, pos in event["fight_refs"]
        ]
        events.append(
            EventModel(
                event_name=event.get("event_name"),
                event_date=event.get("event_date"),
                event_location=event.get("event_location"),
                event_status=event.get("event_status"),
                event_ufcstats_url=event.get("event_ufcstats_url"),
                fight_refs=fight_refs,
            )
        )

    return events


def extract_fights(
    controller: MongoDBController, collection_name: str = "fights"
) -> list[FightModel]:
    """
    Extracts fights from a MongoDB collection.

    Args:
        collection_name (str): The name of the collection to extract fights from.
        controller (MongoDBController): An instance of the MongoDBController class.

    Returns:
        list[FightModel]: A list of FightModel objects representing the extracted fights.
    """
    fights_collection = controller.get_collection(collection_name)
    fights = []
    for fight in fights_collection.find():
        fight_ufcstats_url = fight["fight_ufcstats_url"]
        fighter1 = FighterInfoModel(**fight["fighter1"])
        fighter2 = FighterInfoModel(**fight["fighter2"])
        fight_details = FightDetailsModel(**fight["fight_details"])
        fight_stats = {
            k: RoundStatsModel(
                fighter1=PerFighterRoundStatsModel(**v["fighter1"]),
                fighter2=PerFighterRoundStatsModel(**v["fighter2"]),
            )
            for k, v in fight["fight_stats"].items()
        }
        fights.append(
            FightModel(
                fight_ufcstats_url=fight_ufcstats_url,
                fighter1=fighter1,
                fighter2=fighter2,
                fight_details=fight_details,
                fight_stats=fight_stats,
            )
        )

    return fights
