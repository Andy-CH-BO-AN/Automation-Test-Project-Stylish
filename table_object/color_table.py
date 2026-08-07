import db_utilis.db_utils as db_utils


def search_color(color_code, conn):
    command = "SELECT name FROM stylish_backend.color WHERE code = %s"
    result = db_utils.query_method(command, conn, params=(color_code,))
    return result[0]["name"]


def search_color_code_and_name(color_id, conn):
    command = "SELECT code, name FROM stylish_backend.color WHERE id = %s"
    result = db_utils.query_method(command, conn, params=(color_id,))
    return result[0]
