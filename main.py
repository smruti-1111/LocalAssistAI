from fastapi import FastAPI
from api.routes import router
from database.db import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
