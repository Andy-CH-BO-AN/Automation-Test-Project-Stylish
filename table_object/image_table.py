import db_utilis.db_utils as db_utils


def search_images_by_product_id(product_id, conn):
    command = "SELECT image " \
              "FROM stylish_backend.product_images " \
              "WHERE stylish_backend.product_images.product_id = %s"
    params = f"{product_id}"
    result = db_utils.query_method(command, conn, params)
    return result
