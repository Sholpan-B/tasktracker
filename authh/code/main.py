import fastapi
from fastapi.security import OAuth2PasswordRequestForm

from tortoise.contrib.fastapi import register_tortoise

import services
from db import TORTOISE_ORM


def setup():
    app = fastapi.FastAPI()

    register_tortoise(
        app=app, config=TORTOISE_ORM,
        add_exception_handlers=True,
    )

    return app


app = setup()

#
# @app.post('/api/token')
# async def login(form_data: OAuth2PasswordRequestForm = fastapi.Depends()):
#     user, is_authenticated = services.authenticate_user(form_data.username, form_data.password)
#
#     if is_authenticated:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
#             detail='Incorrect username or password',
#             headers={'WWW-Authenticate': 'Bearer'}
#         )
#     access_token = services.create_access_token({'sub': user['username']})
#     return {'access_token': access_token}
#
#
# @app.get('/api/users/me')
# async def get_current_user(
#         current_user: services.User = fastapi.Depends(services.get_current_user),
# ):
#     return current_user
#

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
