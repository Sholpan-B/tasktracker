import os

db_url = os.getenv('db_url')

SECRET_KEY = '0af457a8f1e6f0d215a378d8effff6dc7e470867f4437cdfccb3118b941ee492'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24