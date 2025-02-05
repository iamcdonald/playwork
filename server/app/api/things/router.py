from typing import Annotated, List
from fastapi import APIRouter, Path, Response, status
from pydantic import BaseModel
from psycopg.rows import class_row
import app.db

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

@router.get("/{id}", response_model=Thing)
async def get(id: Annotated[int, Path(title="The ID of the item to get")]):
    cur = app.db.conn.cursor(row_factory=class_row(Thing))
    cur.execute("""SELECT * FROM things WHERE id = %s;""", (id,))
    return cur.fetchone();

@router.get("", response_model=List[Thing])
async def list():
    cur = app.db.conn.cursor(row_factory=class_row(Thing))
    cur.execute("SELECT * FROM things;")
    return cur.fetchall();

@router.post("", response_model=PostThingResponse)
async def create(thing: PostThing):
    cur = app.db.conn.cursor(row_factory=class_row(PostThingResponse))
    cur.execute("""INSERT INTO things (name) VALUES (%s) RETURNING id;""", (thing.name,))
    app.db.conn.commit();
    return cur.fetchone();
