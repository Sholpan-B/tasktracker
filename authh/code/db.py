from const import db_url

models = ['aerich.models', 'models']


TORTOISE_ORM = {
    'connections': {'default': db_url},
    'apps': {
        'models': {
            'models': models,
            'default_connection': 'default',
        },
    },
}
