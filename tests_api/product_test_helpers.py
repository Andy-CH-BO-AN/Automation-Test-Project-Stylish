from api_objects.delete_product_api import DeleteProductApi
from api_objects.products_search_api import ProductsSearchApi


def product_payload_from_row(row):
    return {
        "category": row["Category"],
        "title": row["Title"],
        "description": row["Description"],
        "price": row["Price"],
        "texture": row["Texture"],
        "wash": row["Wash"],
        "place": row["Place of Product"],
        "note": row["Note"],
        "color_ids": row["ColorIDs"],
        "sizes": row["Sizes"],
        "story": row["Story"],
        "main_image": row["Main Image"],
        "other_images": [row["Other Image 1"], row["Other Image 2"]],
    }


def find_product_by_title(session, title):
    response = ProductsSearchApi(session, title, 0).send()
    assert response.status_code == 200
    return next(
        (product for product in response.json()["data"] if product["title"] == title),
        None,
    )


def product_id(product):
    return product.get("id", product.get("product_id"))


def delete_product_if_exists(session, title):
    product = find_product_by_title(session, title)
    if product is None:
        return None
    return DeleteProductApi(session, product_id(product)).send()
