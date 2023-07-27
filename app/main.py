import uvicorn
from fastapi import FastAPI

from router.router import api_router

from database.base import Base
from database.db import engine


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)