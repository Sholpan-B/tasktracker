import os
import pydantic


database_url = os.getenv('database_url')
# database_url = pydantic.PostgresDsn(os.getenv('database_url'))

minio_url = os.getenv('MINIO_URL')
minio_root_user = os.getenv('MINIO_ROOT_USER')
minio_root_password = os.getenv('MINIO_ROOT_PASSWORD')
minio_bucket_name = os.getenv('MINIO_BUCKET_NAME')
