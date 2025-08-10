import logging
from os import environ

en = environ.get

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

start_position_str = en("START_POSITION", "4,2")
start_position_str = start_position_str.replace(" ", "")
START_POSITION = tuple(map(int, start_position_str.split(",")))

START_DIRECTION = en("START_DIRECTION", "W")

OBSTACLES = {(1, 4), (3, 5), (7, 4)}

# Postgres
POSTGRES_DSN = en(
    "POSTGRES_DSN", "postgresql+asyncpg://user:password@postgres:5432/database"
)
POSTGRES_MIN_SIZE = en("POSTGRES_MIN_SIZE", "5")
POSTGRES_MAX_SIZE = en("POSTGRES_MAX_SIZE", "10")

API_TOKEN = en("API_TOKEN", "my-secret-token")
