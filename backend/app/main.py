from fastapi import FastAPI
from .api import thing
from .db import db
from .publish import publisher

publisher.thread.start()
app = FastAPI()
app.include_router(thing.router)
