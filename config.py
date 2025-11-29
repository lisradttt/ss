import os
from os import getenv
from dotenv import load_dotenv
from OWNER import BOT_TOKEN, OWNER, OWNER_NAME, DATABASE, CHANNEL, GROUP, LOGS, VIDEO

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
user = {}
call = {}
dev = {}
logger = {}
logger_mode = {}
botname = {}
appp = {}
helper = {}



_api_id = getenv("API_ID", 14823185)
try:
    API_ID = int(_api_id) if _api_id else 0
except Exception:
    API_ID = 0

API_HASH = getenv("API_HASH", "68493d4100bf829b3a84a43f0269bed6")
BOT_TOKEN = BOT_TOKEN
MONGO_DB_URL = DATABASE
OWNER = OWNER
OWNER_NAME = OWNER_NAME
CHANNEL = CHANNEL
GROUP = GROUP
LOGS = LOGS
VIDEO = VIDEO
# Optional default photo to be used in thumbnails/placeholder images.
# If not provided via env, reuse the VIDEO (url) string. Some places expect
# a local file path; ensure code checks exists before removing.
PHOTO = getenv("PHOTO", VIDEO)

