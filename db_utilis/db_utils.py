import logging

from pymysql.cursors import DictCursor


def query_method(query, conn, params=None):
    with conn.cursor(cursor=DictCursor) as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()
        logging.info("DB query executed: %s", query)
        return result
