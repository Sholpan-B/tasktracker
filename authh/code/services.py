from datetime import datetime, timedelta

import fastapi as fa
import fastapi.security as fs
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel


SECRET_KEY = '0af457a8f1e6f0d215a378d8effff6dc7e470867f4437cdfccb3118b941ee492'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_db = {
    'johndoe': {
        'fullname': 'John Doe',
        'password': '$2a$12$dO7K8xqyOs4h4CSuO3SHUuRbpSFY0RqfIIoAYSSaTSt0PGOpf7QXq'
    },
}


class Token(BaseModel):
    token: str


class User(BaseModel):
    username: str
    fullname: str
    password: str


pwd_context = CryptContext(schemes=['bcrypt'])

oauth2_scheme = fs.OAuth2PasswordBearer(tokenUrl='')

app = fa.FastAPI()


def verify_password(plain_pass: str, hash_pass: str) -> bool:
    return pwd_context.verify(plain_pass, hash_pass)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(username: str) -> dict:
    if username in fake_db:
        return User(**fake_db[username])


def authenticate_user(username: str, password: str):
    user = fake_db.get(username)

    if not user:
        return user, False

    if not verify_password(password, user['password']):
        return user, False

    return user, True


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    payload = data.copy()

    if expire_delta:
        expire = datetime.now() + expire_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({'exp': expire})
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def get_current_user(token: str = fa.Depends(oauth2_scheme)):
    creds_exception = fa.HTTPException(
        status_code=fa.status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token.get('sub')

        if username is None:
            raise creds_exception

    except JWTError:
        raise creds_exception

    user = get_user(username)

    if user in None:
        raise creds_exception

    return user


# def get_current_active(current_user: User = fa.Depends(get_current_user)):
#     return current_user
