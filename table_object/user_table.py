import db_utilis.db_utils as db_utils


def search_user_info(email, conn):
    command = "SELECT * FROM stylish_backend.user WHERE email = %s"
    user_info = db_utils.query_method(command, conn, params=(email,))
    return user_info[0]
