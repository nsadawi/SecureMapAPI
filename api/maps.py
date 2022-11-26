
from fastapi import status, HTTPException, APIRouter, Depends
from database.db import Map, database
from schema.schema import MapSchemaIn, MapSchemaOut, UserSchemaOut
from typing import List
from auths import get_current_user


router = APIRouter(
    tags = ["Maps"]
)


#@router.get('/maps/', response_model=List[MapSchemaOut])
#async def get_map(current_user:UserSchemaOut = Depends(get_current_user)):
#    query = Map.select()
#    return await database.fetch_all(query=query)


@router.get('/maps/{id}', response_model=MapSchemaOut)
async def get_map(id:int, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Map.select().where(id==Map.c.map_id)
    my_map = await database.fetch_one(query=query)

    if not my_map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Map does not exists")
    return {**my_map}



@router.post('/maps/', status_code=status.HTTP_201_CREATED)
async def insert_data(map:MapSchemaIn, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Map.insert().values(map_id = map.map_id, path=map.path)
    last_record_id = await database.execute(query)

    return {**map.dict(), "id":last_record_id}


@router.put('/maps/{id}/')
async def update_data(id:int, map:MapSchemaIn, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Map.update().where(Map.c.map_id == id).values(map_id = map.map_id, path=map.path)
    await database.execute(query)
    return {**map.dict(), "id":id}


@router.delete('/maps/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id:int, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Map.delete().where(Map.c.map_id == id)
    await database.execute(query)
    return {"message":"Map is deleted"}