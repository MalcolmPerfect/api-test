"""simple fastapi example"""
import sqlite3
import logging
import uvicorn

# from sqlite3 import Cursor, Connection, connect
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Shape(BaseModel):
    name: str
    no_sides: int
    id: int


@app.put("/shapes/init")
def init_db():
    """creates/replaces the database table and initialises with a couple of
    rows of sample data"""
    exec_sql_write("drop table if exists shape")
    exec_sql_write("create table shape(id int, name text, no_sides int)")

    seed_data: list[dict] = [
        {"name": "square", "no_sides": 4, "id": 1},
        {"name": "triangle", "no_sides": 3, "id": 2},
    ]
    insert_shapes(seed_data)


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/shapes/{shape_id}")
def get_shape_by_id(shape_id: int) -> Shape:
    """returns a shape for the id supplied. 404 if not found"""
    results = exec_sql_read("select * from shape where id = ?", shape_id)
    if len(results) == 0:
        raise HTTPException(status_code=404, detail=f"No shape found for id {shape_id}")
    return Shape(**results[0])


def read_shape_by_id(shape_id: int):
    return exec_sql_read("select * from shape where id = ?", shape_id)


def insert_shapes(shapes: list[dict]):
    exec_sql_write(
        "insert into shape(name, no_sides, id) values(:name, :no_sides, :id)", shapes
    )


def update_shapes(shapes: list[dict]):
    exec_sql_write(
        "update shape set name = :name, no_sides = :no_sides where id = :id", shapes
    )


@app.put("/shapes")
def upsert_shape(shape: Shape):
    """Update or insert a shape object. Idempotent"""

    res = read_shape_by_id(shape.id)
    if len(res) == 0:
        insert_shapes([shape.model_dump()])
    else:
        update_shapes([shape.model_dump()])


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


@app.get("/shapes")
def get_all_shapes() -> list[Shape]:
    all_shapes = exec_sql_read("select * from shape")
    return [Shape(**row) for row in all_shapes]


def exec_sql_read(sql: str, *args) -> list[dict]:
    logging.info(f"executing sql {sql} with params {args}")

    con: sqlite3.Connection = get_db_connection()
    cur: sqlite3.Cursor = con.cursor()
    cur.row_factory = dict_factory

    # pass in sql params in tuple form
    res = cur.execute(sql, args).fetchall()
    return res


def exec_sql_write(sql: str, data: list[dict] = None):
    logging.info(f"executing sql {sql} with data {data}")
    con: sqlite3.Connection = get_db_connection()
    cur: sqlite3.Cursor = con.cursor()

    if data is None:
        cur.execute(sql)
    # elif len(data) == 1:
    #     cur.execute(sql, data[0])
    else:
        cur.executemany(sql, data)
    con.commit()


def get_db_connection() -> sqlite3.Connection:
    """return a db conection. In real life this would be injected
    For the moment just returning a new connection every time, again,
    just for simplicity"""
    return sqlite3.connect("shapes.db")


# handy for debugging - put a breakpoint here
if __name__ == "__main__":
    uvicorn.run(app, log_config="logging.ini", log_level=logging.DEBUG)
