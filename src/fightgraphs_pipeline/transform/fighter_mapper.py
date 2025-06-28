import re
from typing import Optional, Any
from fightgraphs_pipeline.models.mongodb_models import FighterModel, FighterImageModel
from fightgraphs_pipeline.utils import gen_id_from_url, convert_date

from fightgraphs_pipeline.models.postgresql_models import (
    FighterEntity,
    FighterRecordEntity,
)


class FighterMapper:
    def __init__(self):
        """
        A stateless mapper class to convert MongoDB fighter data into PostgreSQL entities.
        It contains pure functions for transformation.
        """
        pass

    def convert_height(self, height: Optional[str]) -> Optional[float]:
        """
        Convert height from feet and inches to centimeters.
        """
        if not height or height == "--":
            return None
        match = re.match(r"(\d+)'\s*(\d+)", height)
        if match:
            feet = int(match.group(1))
            inches = int(match.group(2))
            total_inches = feet * 12 + inches
            cm = round(total_inches * 2.54, 2)
            return cm
        return None

    def convert_weight(self, weight: Optional[str]) -> Optional[float]:
        """
        Convert weight from pounds to kilograms.
        """
        if not weight or weight == "--":
            return None
        match = re.search(r"(\d+(\.\d+)?)", weight)
        if match:
            pounds = float(match.group(1))
            kg = round(pounds * 0.453592, 2)
            return kg
        return None

    def convert_reach(self, reach: Optional[str]) -> Optional[float]:
        """
        Convert reach from inches to centimeters.
        """
        if not reach or reach == "--":
            return None
        match = re.match(r"(\d+(\.\d+)?)", reach)
        if match:
            inches = float(match.group(1))
            cm = round(inches * 2.54, 2)
            return cm
        return None

    def convert_record(self, record: Optional[str]) -> dict:
        """
        Convert fighter record string to a standardized format of wins, losses, draws, no_contests.
        """
        if not record or record == "--":
            return {"wins": 0, "losses": 0, "draws": 0, "no_contests": 0}

        match = re.search(r"(\d+)-(\d+)-(\d+)(?:\s*\((\d+)\s*NC\))?", record)
        if match:
            wins = int(match.group(1))
            losses = int(match.group(2))
            draws = int(match.group(3))
            no_contests = int(match.group(4)) if match.group(4) else 0
            return {
                "wins": wins,
                "losses": losses,
                "draws": draws,
                "no_contests": no_contests,
            }
        return {"wins": 0, "losses": 0, "draws": 0, "no_contests": 0}

    def map_fighter_to_entity(
        self,
        fighter_model: FighterModel,
        fighter_image_model: Optional[FighterImageModel] = None,
    ) -> tuple[FighterEntity, FighterRecordEntity]:
        """
        Maps a FighterModel to a FighterEntity for PostgreSQL.
        """
        if not fighter_model:
            raise ValueError("Fighter model cannot be None")
        if not fighter_model.fighter_ufcstats_url:
            raise ValueError("Fighter model must have a valid UFCStats URL")
        id = gen_id_from_url(fighter_model.fighter_ufcstats_url)
        first_name = fighter_model.first_name
        last_name = fighter_model.last_name
        nickname = fighter_model.nickname
        date_of_birth = convert_date(fighter_model.date_of_birth)
        height_cm = self.convert_height(fighter_model.height)
        weight_kg = self.convert_weight(fighter_model.weight)
        reach_cm = self.convert_reach(fighter_model.reach)
        stance = fighter_model.stance
        image_url = (
            fighter_image_model.fighter_image_url
            if fighter_image_model is not None
            else None
        )
        ufcstats_url = fighter_model.fighter_ufcstats_url
        fighter_record = self.convert_record(fighter_model.fighter_record)

        fighter_entity = FighterEntity(
            id=id,
            first_name=first_name,
            last_name=last_name,
            nickname=nickname,
            date_of_birth=date_of_birth,
            height_cm=height_cm,
            weight_kg=weight_kg,
            reach_cm=reach_cm,
            stance=stance,
            image_url=image_url,
            ufcstats_url=ufcstats_url,
        )
        fighter_record_entity = FighterRecordEntity(
            fighter_id=id,
            wins=fighter_record["wins"],
            losses=fighter_record["losses"],
            draws=fighter_record["draws"],
            no_contests=fighter_record["no_contests"],
        )

        return fighter_entity, fighter_record_entity

    def map_fighters_to_entities(
        self,
        fighter_models: list[FighterModel],
        fighter_images: list[FighterImageModel],
    ) -> list[dict[str, Any]]:
        """
        Maps a list of FighterModel objects to a list of dicts with FighterEntity and FighterRecordEntity.

        Args:
            fighter_models (list[FighterModel]): List of fighter models from MongoDB.
            fighter_images (list[FighterImageModel]): List of fighter image models from MongoDB.

        Returns:
            list[dict[str, Any]]: List of dictionaries containing FighterEntity and FighterRecordEntity.
        """
        image_lookup = {
            gen_id_from_url(img.fighter_ufcstats_url): img for img in fighter_images
        }

        fighter_and_record_entities = []
        for fighter_model in fighter_models:
            fighter_id = gen_id_from_url(fighter_model.fighter_ufcstats_url)
            fighter_image_model = image_lookup.get(fighter_id, None)

            fighter_entity, fighter_record_entity = self.map_fighter_to_entity(
                fighter_model, fighter_image_model
            )

            fighter_and_record_entities.append(
                {
                    "fighter_entity": fighter_entity,
                    "fighter_record_entity": fighter_record_entity,
                }
            )

        return fighter_and_record_entities
