from pydantic import BaseModel
from typing import Union


class MapSchemaIn(BaseModel):
    map_id:int
    path:str


class MapSchemaOut(MapSchemaIn):
    map_id: int
    path: str


class UserSchemaIn(BaseModel):
    username:str
    password:str


class UserSchemaOut(BaseModel):
    id:int
    username:str


class LoginSchema(BaseModel):
    username:str
    password:str



class TokenData(BaseModel):
    username: Union[str, None] = None