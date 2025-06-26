from fightgraphs_pipeline.models.mongodb_models import (
	FighterModel,
	EventModel,
	FighterImageModel,
	FightDetailsModel,
	PerFighterStatsModel,
	FightModel)

from fightgraphs_pipeline.database.mongodb_controller import MongoDBController


def extract_fighters(controller: MongoDBController, collection_name: str = "fighters") -> list[FighterModel]:
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






