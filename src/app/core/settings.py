import os
import pydantic


database_url = os.getenv('database_url')
# database_url = pydantic.PostgresDsn(os.getenv('database_url'))
