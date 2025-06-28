import re

from typing import Optional, Tuple, Dict
from fightgraphs_pipeline.models.mongodb_models import EventModel, FightRefModel
from fightgraphs_pipeline.utils import gen_id_from_url, convert_date

from fightgraphs_pipeline.models.postgresql_models import EventEntity


class EventMapper:
    """
    Mapper class to convert MongoDB EventModel to PostgreSQL EventEntity.
    """

    def __init__(self):
        pass

    def map_event_to_postgres(
        self, event: EventModel
    ) -> tuple[EventEntity, list[dict]]:
        """
        Maps a MongoDB EventModel to a PostgreSQL EventEntity.

        Args:
            event (EventModel): The MongoDB event model to map.

        Returns:
            EventEntity: The mapped PostgreSQL event entity.
        """
        if not event.event_name or not event.event_date or not event.event_location:
            raise ValueError("Event must have name, date, and location")
        id = gen_id_from_url(event.event_name)
        name = event.event_name
        date = convert_date(event.event_date)
        location = event.event_location
        ufcstats_url = event.event_ufcstats_url
        promotion_id = 1  ## UFC is the only promotion in this context
        event_entity = EventEntity(
            id=id,
            name=name,
            date=date,
            location=location,
            ufcstats_url=ufcstats_url,
            promotion_id=promotion_id,
        )

        fight_refs = self.map_fight_refs(id, event.fight_refs)
        return event_entity, fight_refs

    def map_fight_refs(
        self, event_id: int, fight_refs: list[FightRefModel]
    ) -> list[dict]:
        """
        Maps fight references from MongoDB to PostgreSQL format.

        Args:
            event_id (int): The ID of the event.
            fight_refs (list[FightRefModel]): List of fight reference models.

        Returns:
            list[Tuple[int, str]]: List of tuples containing fight ID and card position.
        """
        mapped_refs = []
        for ref in fight_refs:
            if not ref.fight_ufcstats_url:
                ufcstats_url = None
            else:
                ufcstats_url = ref.fight_ufcstats_url
            if not ref.card_position:
                card_position = None
            else:
                card_position = ref.card_position
            fight_id = gen_id_from_url(ufcstats_url)
            mapped_refs.append(
                {
                    "event_id": event_id,
                    "fight_id": fight_id,
                    "card_position": card_position,
                }
            )
        return mapped_refs
