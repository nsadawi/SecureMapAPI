from fastapi import APIRouter, status
from schema.schema import UserSchemaIn, UserSchemaOut
from database.db import User, database
from passlib.hash import sha256_crypt
from typing import List


router = APIRouter(
    tags = ["Users"]
)


@router.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserSchemaOut)
async def insert_user(user:UserSchemaIn):
    hashed_password = sha256_crypt.hash(user.password)
    query = User.insert().values(username=user.username, password=hashed_password)
    last_record_id = await database.execute(query=query)

    return {**user.dict(), "id":last_record_id}


@router.get('/users/', response_model=List[UserSchemaOut])
async def get_users():
    query = User.select()
    return await database.fetch_all(query=query)