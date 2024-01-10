from datetime import datetime, timedelta

import fastapi as fa
import fastapi.security as fs
from jose import jwt, JWTError
from passlib.context import CryptContext

import schemas
import const
from repo import UserRepo

pwd_context = CryptContext(schemes=['bcrypt'])

oauth2_scheme = fs.OAuth2PasswordBearer(tokenUrl='/api/auth/login')


class TokenService:
    def create_token(self, data: schemas.TokenData, expires_delta: timedelta) -> str:
        payload = {
            'sub': str(data.sub),
            'exp': datetime.utcnow() + expires_delta,
        }

        return jwt.encode(payload, const.SECRET_KEY, algorithm=const.ALGORITHM)

    def create_tokens(self, data: schemas.TokenData):
        access = self.create_token(
            data, expires_delta=timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh = self.create_token(
            data, expires_delta=timedelta(hours=const.REFRESH_TOKEN_EXPIRE_HOURS),
        )
        return {'access_token': access, 'refresh_token': refresh}

    def decode_token(self, token:str) -> schemas.TokenData:
        creds_exception = fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

        try:
            decoded_token_payload = jwt.decode(token, const.SECRET_KEY, algorithms=[const.ALGORITHM])
            user_id = decoded_token_payload.get('sub')

            if user_id is None:
                raise creds_exception
        except JWTError:
            raise creds_exception

        return schemas.TokenData(**decoded_token_payload)

    def refresh_token(self, refresh_token: str):
        token_data = self.decode_token(refresh_token)
        access = self.create_token(token_data, timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES))
        return {'access_token': access, 'refresh_token': refresh_token}


token_service = TokenService()


class AuthService:
    def __init__(self) -> None:
        self.user_repo = UserRepo()

    def verify_password(self, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, username: str, password: str):
        users = await self.user_repo.get_list(username=username)

        if users and self.verify_password(password, users[0].password):
            return users[0]

    async def login(self, data: schemas.LoginRequestModel):
        user = await self.authenticate_user(data.username, data.password)

        if not user:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_404_NOT_FOUND,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'},

            )
        return token_service.create_tokens(schemas.TokenData(sub=user.id))

    async def get_current_user(self, token: str = fa.Security(oauth2_scheme)):
        token_data = token_service.decode_token(token)
        user = await self.user_repo.get(id=token_data.sub)

        if token_data.role != 'system_consumer':
            raise fa.HTTPException(
                status_code=fa.status.HTTP_401_UNAUTHORIZED,
                detail='Insufficient permissions',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        return user


auth_service = AuthService()
