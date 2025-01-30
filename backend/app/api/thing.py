from typing import Annotated, List
from fastapi import APIRouter, Path, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.db import db
from kafka import KafkaConsumer
from psycopg.rows import class_row
from app.conf import conf



class Thing(BaseModel):
    id: int
    name: str

class PostThing(BaseModel):
    name: str

class PostThingResponse(BaseModel):
    id: int

router = APIRouter(prefix="/things")

@router.get("/listen")
async def listen():
    headers = {
        "Content-Type": "text/plain",
        "Grip-Hold": "stream",
        "Grip-Channel" : "things"
    }
    return Response(status_code=status.HTTP_200_OK, headers=headers);
    # return RedirectResponse(url="http://{host}:7999".format(host=conf.PUSHPIN_EXTERNAL_HOST));

@router.get("/{id}", response_model=Thing)
async def get(id: Annotated[int, Path(title="The ID of the item to get")]):
    cur = db.conn.cursor(row_factory=class_row(Thing))
    cur.execute("""SELECT * FROM things WHERE id = %s;""", (id,))
    return cur.fetchone();

@router.get("", response_model=List[Thing])
async def list():
    cur = db.conn.cursor(row_factory=class_row(Thing))
    cur.execute("SELECT * FROM things;")
    return cur.fetchall();

@router.post("", response_model=PostThingResponse)
async def create(thing: PostThing):
    cur = db.conn.cursor(row_factory=class_row(PostThingResponse))
    cur.execute("""INSERT INTO things (name) VALUES (%s) RETURNING id;""", (thing.name,))
    db.conn.commit();
    return cur.fetchone();
