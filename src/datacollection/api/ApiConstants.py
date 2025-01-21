import os
from dotenv import load_dotenv

load_dotenv()

""" This module contains the constants used in API calls """

REDDIT_APP_ID = os.getenv("REDDIT_APP_ID")
REDDIT_SECRET_KEY = os.getenv("REDDIT_SECRET_KEY")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
AUTH_URL = "https://www.reddit.com/api/v1/access_token"
AUTH_TYPE_PASSWORD = "password"
data = {
    "grant_type": AUTH_TYPE_PASSWORD,
    "username": REDDIT_USERNAME,
    "password": REDDIT_PASSWORD
}

REDDIT_LATEST_DATA_CAP = 200
REDDIT_LATEST_SUBREDDIT_DATA_CAP = 200

MAXIMUM_AUTHENTICATION_ATTEMPTS = 3
MAXIMUM_QUERY_ATTEMPTS = 5
MAXIMUM_COMMENT_RETRIEVAL_ATTEMPTS = 5

REQUEST_SUCCESS_CODE = 200
REQUEST_FORBIDDEN_CODE = 403
REQUEST_EXCEEDED_CODE = 429