import db_utilis.db_utils as db_utils


def search_variants_by_product_id(product_id, conn):
    command = "SELECT color_id, size, stock " \
              "FROM stylish_backend.variant " \
              "WHERE stylish_backend.variant.product_id = %s"
    params = f"{product_id}"
    result = db_utils.query_method(command, conn, params)
    return result
