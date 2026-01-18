from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers.users import router as user_router
from routers.characters import router as character_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="API for Game",lifespan=lifespan)

app.include_router(user_router)
app.include_router(character_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)


