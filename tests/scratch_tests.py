from fightgraphs_pipeline.extract.extraction import (
    extract_fighters,
    extract_fighter_images,
    extract_events,
    extract_fights,
)
from fightgraphs_pipeline.transform.fighter_mapper import FighterMapper
from fightgraphs_pipeline.utils import get_controllers
import json

# Old direct MongoDBController usage (can be removed if using get_controllers)
mongo_controller, postgres_controller = get_controllers()


fighters = extract_fighters(mongo_controller)
print("Fighters:")
for i in range(min(5, len(fighters))):
    print(json.dumps(fighters[i].model_dump(), indent=4))

# Extract and print fighter images
fighter_images = extract_fighter_images(mongo_controller)
print("\nFighter Images:")
for i in range(min(5, len(fighter_images))):
    print(json.dumps(fighter_images[i].model_dump(), indent=4))

# Extract and print events
events = extract_events(mongo_controller)
print("\nEvents:")
for i in range(min(5, len(events))):
    print(json.dumps(events[i].model_dump(), indent=4))

# Extract and print fights
fights = extract_fights(mongo_controller)
print("\nFights:")
for i in range(min(2, len(fights))):  # fights may be large, print 2
    print(json.dumps(fights[i].model_dump(), indent=4))

# --- Added ETL pipeline code below ---


fighters = extract_fighters(mongo_controller)
fighter_images = extract_fighter_images(mongo_controller)
fighter_mapper = FighterMapper()

fighter_and_record_entities = fighter_mapper.map_fighters_to_entities(
    fighters, fighter_images
)

c = 0
for entity in fighter_and_record_entities:
    fighter_entity = entity["fighter_entity"]
    fighter_record_entity = entity["fighter_record_entity"]
    fighter_dict = {
        c.name: getattr(fighter_entity, c.name)
        for c in fighter_entity.__table__.columns
    }
    fighter_record_dict = {
        c.name: getattr(fighter_record_entity, c.name)
        for c in fighter_record_entity.__table__.columns
    }
    print(json.dumps(fighter_dict, indent=4, default=str))
    print(json.dumps(fighter_record_dict, indent=4, default=str))
    c += 1
    if c >= 5:
        break
