import hashlib
from typing import Optional, Tuple
from datetime import datetime, date
from dotenv import load_dotenv
import os
from fightgraphs_pipeline.database.postgres_controller import PostgresController
from fightgraphs_pipeline.database.mongodb_controller import MongoDBController


def gen_id_from_url(url: Optional[str], max_digits: int = 9) -> int:
    """
    Generate a unique numeric ID from a URL using SHA-256 hash.
    The result is truncated to `max_digits` digits for database compatibility.
    """
    if not url:
        raise ValueError("URL must not be None or empty")

    hash_object = hashlib.sha256(url.encode("utf-8"))
    # Convert hash to integer
    hash_int = int(hash_object.hexdigest(), 16)
    # Truncate to desired number of digits
    numeric_id = int(str(hash_int)[-max_digits:])
    return numeric_id


def convert_date(date: Optional[str]) -> Optional[date]:
    """
    Convert date of birth string to a standardized format (YYYY-MM-DD).
    """
    if not date or date == "--":
        return None
    try:
        return datetime.strptime(date, "%b %d, %Y").date()
    except ValueError:
        return None


def get_controllers() -> Tuple[MongoDBController, PostgresController]:
    """
    Initialize and return MongoDB and PostgreSQL controllers.
    """
    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI")
    mongo_db = os.getenv("MONGODB_DATABASE")
    if not mongo_uri or not mongo_db:
        raise ValueError("MONGODB_URI and MONGODB_DATABASE must be set in .env file")
    mongo_controller = MongoDBController(mongo_uri, mongo_db)
    postgres_uri = os.getenv("POSTGRES_URI")
    postgres_db = os.getenv("POSTGRES_DATABASE")
    if not postgres_uri or not postgres_db:
        raise ValueError("POSTGRES_URI and POSTGRES_DATABASE must be set in .env file")
    postgres_controller = PostgresController(postgres_uri, postgres_db)
    return mongo_controller, postgres_controller
