from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
BOT_ID: str = BOT_TOKEN.split(":")[0]

ADMIN: int = int(env.str("ADMIN"))
CLIENT_ID = env.str("CLIENT_ID")
API_KEY = env.str("API_KEY")
PARK_ID = env.str("PARK_ID")

API_BASE_URL = env.str("API_BASE_URL")