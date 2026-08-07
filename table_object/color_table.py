import logging

import db_utilis.db_utils as db_utils


def search_color(color_code, conn):
    logging.info(color_code)
    command = f"SELECT name FROM stylish_backend.color WHERE code = '{color_code}'"
    result = db_utils.query_method(command, conn, params=None)
    return result[0]["name"]


def search_color_code_and_name(color_id, conn):
    command = f"SELECT code, name FROM stylish_backend.color WHERE id = '{color_id}'"
    result = db_utils.query_method(command, conn, params=None)
    return result[0]
