import main
from main import Shape
from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException


# TODO refactor per the following to pass in the connection and avoid patch
# def test_exec_sql2():
#     mock_conn = MagicMock()
#     mock_return_val = [{"name": "square", "no_sides": 4, "id": 1}]
#     mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = (
#         mock_return_val
#     )
#     result = main.exec_sql2(mock_conn, "select * from shape")
#     assert result == mock_return_val


@patch("main.get_db_connection")
def test_exec_sql_read(mock_db_connection):
    mock_return_val = [{"name": "square", "no_sides": 4, "id": 1}]

    mock_db_connection.return_value.cursor.return_value.execute.return_value.fetchall.return_value = (
        mock_return_val
    )
    result = main.exec_sql_read("select * from shape")
    assert result == mock_return_val


@patch("main.get_db_connection")
def test_exec_sql_write_no_data(mock_db_connection: MagicMock):
    main.exec_sql_write("blah sql")
    mock_db_connection.return_value.cursor.return_value.execute.assert_called_once_with(
        "blah sql"
    )
    mock_db_connection.return_value.commit.assert_called_once()
    # assert result == mock_return_val


@patch("main.get_db_connection")
def test_exec_sql_write_data(mock_db_connection: MagicMock):
    data: list[dict] = [{"name": "square", "no_sides": 4, "id": 1}]
    main.exec_sql_write("blah sql", data)
    mock_db_connection.return_value.cursor.return_value.executemany.assert_called_once_with(
        "blah sql", [{"name": "square", "no_sides": 4, "id": 1}]
    )
    mock_db_connection.return_value.commit.assert_called_once()


@patch("main.exec_sql_read")
def test_get_shape_by_id_with_result(mock_sql_read: MagicMock):
    mock_sql_read.return_value = [{"name": "square", "no_sides": 4, "id": 1}]
    res: Shape = main.get_shape_by_id(123)
    assert type(res) is Shape
    assert res == Shape(**{"name": "square", "no_sides": 4, "id": 1})


@patch("main.exec_sql_read")
def test_get_shape_by_id_without_result(mock_sql_read: MagicMock):
    mock_sql_read.return_value = []
    with pytest.raises(HTTPException) as ex_info:
        main.get_shape_by_id(123)

    assert ex_info.value.status_code == 404
    assert ex_info.value.detail == "No shape found for id 123"
    # assert type(res) is Shape
    # assert res == Shape(**{"name": "square", "no_sides": 4, "id": 1})


# def get_shape_by_id(shape_id: int) -> Shape:
#     """returns a shape for the id supplied. 404 if not found"""
#     results = exec_sql_read("select * from shape where id = ?", shape_id)
#     if len(results) == 0:
#         raise HTTPException(status_code=404, detail=f"No shape found for id {shape_id}")
#     return Shape(**results[0])


def test_dict_factory():
    cursor_mock = MagicMock()

    cursor_mock.description = [["name"], ["no_sides"], ["id"]]
    row = ["triangle", 3, 1]

    result = main.dict_factory(cursor_mock, row)
    assert result == {"name": "triangle", "no_sides": 3, "id": 1}


@patch("main.insert_shapes")
@patch("main.read_shape_by_id")
def test_upsert_shape_insert(
    mock_read_shape_by_id: MagicMock, mock_insert_shapes: MagicMock
):
    shape: Shape = Shape(name="triangle", no_sides=3, id=5)
    mock_read_shape_by_id.return_value = []
    main.upsert_shape(shape)
    mock_read_shape_by_id.assert_called_once_with(shape.id)
    mock_insert_shapes.assert_called_once_with([shape.model_dump()])


@patch("main.update_shapes")
@patch("main.read_shape_by_id")
def test_upsert_shape_update(
    mock_read_shape_by_id: MagicMock, mock_update_shapes: MagicMock
):
    shape: Shape = Shape(name="triangle", no_sides=3, id=5)
    mock_read_shape_by_id.return_value = [shape.model_dump()]
    main.upsert_shape(shape)
    mock_read_shape_by_id.assert_called_once_with(shape.id)
    mock_update_shapes.assert_called_once_with([shape.model_dump()])
