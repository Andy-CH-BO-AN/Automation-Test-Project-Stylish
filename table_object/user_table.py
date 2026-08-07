import db_utilis.db_utils as db_utils


def search_user_info(email, conn):
    command = f"SELECT * FROM stylish_backend.user WHERE email = '{email}';"
    user_info = db_utils.query_method(command, conn)
    return user_info[0]
