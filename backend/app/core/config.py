import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY","")
    CLERK_PUBLISHABLE_KEY: str = os.getenv("CLERK_PUBLISHABLE_KEY","")
    CLERK_WEEBHOOK_SECRET: str = os.getenv("CLERK_WEEBHOOK_SECRET","")
    CLERK_JWS_URL: str = os.getenv("CLERK_JWS_URL","")

    DATABASE_URL: str = os.getenv("DATABASE_URL","")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL","")

    FREE_TIER_MEMBERSHP_LIMIT:int = 2
    PRO_TIER_MEMBERSHP_LIMIT:int = 0 #unlimited


settings = Config()