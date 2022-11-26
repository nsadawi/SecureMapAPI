from fastapi import APIRouter, status, HTTPException, Depends
from schema.schema import LoginSchema, TokenData
from database.db import User, database
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    tags = ["Login"]
)


async def get_current_user(token: str = Depends((oauth2_schema))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers = {"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(weeks=1)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/login/')
async def login_user(request:OAuth2PasswordRequestForm = Depends()):
    query = User.select().where(User.c.username == request.username)
    myuser = await database.fetch_one(query=query)

    if not myuser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not sha256_crypt.verify(request.password, myuser.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    access_token = create_access_token(
        data = {"sub":myuser.username}
    )
    return {"access_token":access_token, "token_type":"bearer"}
