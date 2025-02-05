from fastapi import FastAPI
import app.api.things


server = FastAPI()
publisher = app.api.things.Publisher();

@server.on_event("startup")
def start_publishers():
    publisher.start()

server.include_router(app.api.things.router)
