import fastapi as fa
from fastapi.security import OAuth2PasswordRequestForm

import schemas
import services
from repo import UserRepo

router = fa.APIRouter(prefix='/api', tags=['user'])
repo = UserRepo()


@router.get('/users')
async def get_users(params: schemas.UserAllOptionalSchema = fa.Depends()):
    return await repo.get_list(**params.dict(exclude_none=True))


@router.get('/users/{id}')
async def get_user(id: int):
    return await repo.get(id=id)


@router.post('/users')
async def create_user(data: schemas.CreateUserSchema):
    return await repo.create(**data.dict(exclude_none=True))


@router.post('/auth/login')
async def login(form_data: OAuth2PasswordRequestForm = fa.Depends()):
    return await services.auth_service.login(form_data)


@router.get('/auth/users/me')
async def read_users_me(user: dict = fa.Depends(services.auth_service.get_current_user)):
    return user


@router.post('/auth/refresh')
async def refresh_token(
        data: dict,
        user: dict = fa.Depends(services.auth_service.get_current_user),
):
    return await services.token_service.refresh_token(data['refresh_token'])
