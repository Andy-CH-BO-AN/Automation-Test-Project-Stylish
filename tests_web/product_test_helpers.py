from table_object.color_table import search_color


def resolve_product_color(product_detail, conn):
    detail = dict(product_detail)
    color_code = detail.pop("product_color_code")
    detail["product_color"] = search_color(color_code, conn)
    return detail
