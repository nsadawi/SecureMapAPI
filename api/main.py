import uvicorn
from fastapi import FastAPI
from database.db import metadata, database, engine
import maps
import users
import auths

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()




app.include_router(router=maps.router)
app.include_router(router=users.router)
app.include_router(router=auths.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info", reload=True)