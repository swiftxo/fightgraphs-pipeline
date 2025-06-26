from fightgraphs_pipeline.extract.extraction import extract_fighters
from fightgraphs_pipeline.database.mongodb_controller import MongoDBController
from dotenv import load_dotenv
import os, json

load_dotenv()


controller = MongoDBController(
	mongo_uri=os.getenv("MONGODB_URI"), db_name=os.getenv("MONGODB_DATABASE")
)
fighters = extract_fighters(controller)

for i in range(5):
	print(json.dumps(fighters[i].model_dump(), indent=4))