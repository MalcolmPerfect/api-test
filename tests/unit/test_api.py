import main
from unittest.mock import patch, MagicMock

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
