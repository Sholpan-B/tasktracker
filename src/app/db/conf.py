# try:

from settings import database_url
import db.models

models = ['aerich.models', 'db.models']

# except ImportError:
#     from src.app.settings import database_url
#
#     models = ['aerich.models', 'src.app.db.models']

TORTOISE_ORM = {
    'connections': {'default': database_url},
    'apps': {
        'models': {
            'models': models,
            'default_connection': 'default',
        },
    },
}
