import os
from dotenv import load_dotenv

# Load environment variables from the .env file into the application's environment.
load_dotenv()

# The Config class is responsible for loading and storing all the configuration settings for the application. 
# It reads environment variables and provides default values if they are not set. 
# This includes keys for Clerk authentication, database connection URL, frontend URL, and membership limits for different tiers of service. 
# The settings instance of the Config class can be imported and used throughout the application to access these configuration values.
class Config:
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY","")
    CLERK_PUBLISHABLE_KEY: str = os.getenv("CLERK_PUBLISHABLE_KEY","")
    CLERK_WEEBHOOK_SECRET: str = os.getenv("CLERK_WEEBHOOK_SECRET","")
    CLERK_JWS_URL: str = os.getenv("CLERK_JWS_URL","")

    DATABASE_URL: str = os.getenv("DATABASE_URL","")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL","")

    FREE_TIER_MEMBERSHP_LIMIT:int = 2
    PRO_TIER_MEMBERSHP_LIMIT:int = 0 #unlimited

# Create a global instance of the Config class that can be imported and used throughout the application to access configuration settings.
settings = Config()