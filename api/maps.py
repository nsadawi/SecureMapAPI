
from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.responses import FileResponse

from database.db import Map, database
from schema.schema import MapSchemaIn, MapSchemaOut, UserSchemaOut
#from typing import List
from auths import get_current_user

from cryptography.fernet import Fernet

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Map does not exist")
    return {**my_map}

@router.get('/mapdownload/{id}', responses={200: {"description": "A map.", "content" : {"image/png" : {"example" : "No example available."}}}})
async def download_map(id:int, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Map.select().where(id==Map.c.map_id)
    my_map = await database.fetch_one(query=query)

    if not my_map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Map does not exist")
    
    # opening the key
    with open('/home/ubuntu/filekey.key', 'rb') as filekey:
        key = filekey.read()
    
    # using the key
    fernet = Fernet(key)
 
    # opening the encrypted file
    with open(my_map['path'], 'rb') as enc_file:
        encrypted = enc_file.read()
 
    # decrypting the file
    decrypted = fernet.decrypt(encrypted)
    
    return FileResponse(decrypted, media_type="image/png", filename="mapxyz.png")


"""
@app.get("/cat", responses={200: {"description": "A picture of a cat.", "content" : {"image/jpeg" : {"example" : "No example available. Just imagine a picture of a cat."}}}})
def cat():
    file_path = os.path.join(path, "files/cat.jpg")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg", filename="mycat.jpg")
    return {"error" : "File not found!"}
"""

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
