"""simple fastapi example"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
import sqlite3
from sqlite3 import Cursor, Connection


class Shape(BaseModel):
    name: str
    no_sides: int
    id: int


app = FastAPI()


def init_db():
    con = sqlite3.connect("shapes.db")
    cur = con.cursor()
    cur.execute("drop table if exists shape")
    cur.execute("create table shape(id int, name text, no_sides int)")

    seed_data: Tuple = (
        {"name": "square", "no_sides": 4, "id": 1},
        {"name": "triangle", "no_sides": 3, "id": 2},
    )
    cur.executemany(
        "insert into shape(name, no_sides, id) values(:name, :no_sides, :id)", seed_data
    )
    con.commit()


init_db()


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/shapes/{shape_id}")
def get_shape_by_id(shape_id: int) -> Shape:
    # raise HTTPException(status_code=404, detail=f"No shape found for id {shape_id}")
    con: Connection = sqlite3.connect("shapes.db")
    cur: Cursor = con.cursor()
    cur.row_factory = dict_factory
    result = cur.execute("select * from shape where id = ?", (shape_id,)).fetchone()
    # return [Shape(**row) for row in results]
    return Shape(**result)


@app.post("/shapes")
def post_shape(shape: Shape):
    con = sqlite3.connect("shapes.db")
    cur = con.cursor()
    cur.execute(
        "insert into shape(name, no_sides, id) values(:name, :no_sides, :id)",
        shape.model_dump(),
    )
    con.commit()


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    # return {key: value for key, value in zip(fields, row)}
    return dict(zip(fields, row))


@app.get("/shapes")
def get_all_shapes() -> List[Shape]:
    con: Connection = sqlite3.connect("shapes.db")
    cur: Cursor = con.cursor()
    cur.row_factory = dict_factory
    results = cur.execute("select * from shape").fetchall()
    return [Shape(**row) for row in results]
