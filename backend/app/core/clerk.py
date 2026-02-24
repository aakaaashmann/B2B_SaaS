from clerk_backend_api import Clerk
from app.core.config import settings

# This file initializes the Clerk SDK with the secret key from the config
#provides a global instance of the Clerk client that can be used throughout the application to authenticate requests and manage user sessions.
clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
