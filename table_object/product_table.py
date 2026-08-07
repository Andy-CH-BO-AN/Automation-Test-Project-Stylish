import logging

import db_utilis.db_utils as db_utils


def search_products_name(keyword, conn):
    command = "SELECT title FROM stylish_backend.product WHERE title LIKE %s"
    params = f"%{keyword}%"
    result = db_utils.query_method(command, conn, params)
    result_list = [row['title'] for row in result]
    return result_list


def search_products_detail_by_id(product_id, conn):
    command = "SELECT * " \
              "FROM stylish_backend.product " \
              "WHERE stylish_backend.product.id = %s"
    params = f"{product_id}"
    result = db_utils.query_method(command, conn, params)
    return result


def search_random_product_id(conn):
    command = "SELECT id FROM stylish_backend.product " \
              "ORDER BY RAND ( ) LIMIT 1"
    result = db_utils.query_method(command, conn)
    return result[0]['id']


def search_products_detail_by_keyword(keyword, conn):
    command = "SELECT * " \
              "FROM stylish_backend.product " \
              "WHERE stylish_backend.product.title LIKE %s"

    params = f"%{keyword}%"
    result = db_utils.query_method(command, conn, params)
    return result


def search_products_detail_by_category(category, conn):
    command = "SELECT * " \
              "FROM stylish_backend.product " \
              "WHERE stylish_backend.product.category = %s"

    params = f"{category}"
    result = db_utils.query_method(command, conn, params)
    return result
