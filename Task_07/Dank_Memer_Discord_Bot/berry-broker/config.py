import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Database configuration
DB_NAME = os.getenv("DATABASE_PATH", "berry_broker.db")
DB_PATH = BASE_DIR / DB_NAME

# Discord configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ONE_PIECE_API_KEY = os.getenv("ONE_PIECE_API_KEY", "")

# Economy settings
DEFAULT_WALLET = 1000
DAILY_REWARD_MIN = 100
DAILY_REWARD_MAX = 500
DAILY_COOLDOWN_HOURS = 24

# Raid settings
BASE_RAID_SUCCESS_CHANCE = 0.50
RAID_STEAL_PERCENTAGE = 0.20
RAID_PENALTY_PERCENTAGE = 0.10
MIN_RAID_AMOUNT = 100
RAID_COOLDOWN_MINUTES = 60

# API settings
API_TIMEOUT = 10