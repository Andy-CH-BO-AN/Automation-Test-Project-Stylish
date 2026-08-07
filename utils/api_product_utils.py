import logging
import os

from api_objects.products_category_api import ProductsCategoryApi
from api_objects.products_search_api import ProductsSearchApi
from table_object.color_table import search_color_code_and_name
from table_object.image_table import search_images_by_product_id
from table_object.variant_table import search_variants_by_product_id


def get_all_pages_products(session, pages, *, keyword=None, category=None):
    if (keyword is None) == (category is None):
        raise ValueError("Provide exactly one of keyword or category")

    products = []
    for paging in range(pages):
        if keyword is not None:
            response = ProductsSearchApi(session, keyword, paging).send()
        else:
            response = ProductsCategoryApi(session, category, paging).send()

        assert response.status_code == 200
        products.extend(response.json()["data"])

        if paging < pages - 1:
            logging.info("paging: %s pages: %s", paging, pages)
            assert response.json()["next_paging"] == paging + 1

    return products


def normalize_db_product_detail(db_product_detail, conn):
    product = dict(db_product_detail)
    product_id = product["id"]
    domain = os.getenv("DOMAIN", "").rstrip("/")

    main_image = product["main_image"]
    product["main_image"] = f"{domain}/assets/{product_id}/{main_image}"

    product["images"] = [
        f"{domain}/assets/{product_id}/{row['image']}"
        for row in search_images_by_product_id(product_id, conn)
    ]

    colors = []
    sizes = []
    variants = []
    color_cache = {}

    for raw_variant in search_variants_by_product_id(product_id, conn):
        variant = dict(raw_variant)
        color_id = variant.pop("color_id")

        if color_id not in color_cache:
            color_cache[color_id] = search_color_code_and_name(color_id, conn)
        color = dict(color_cache[color_id])

        variant["color_code"] = color["code"]
        variants.append(variant)

        if color not in colors:
            colors.append(color)
        if variant["size"] not in sizes:
            sizes.append(variant["size"])

    product["variants"] = variants
    product["colors"] = colors
    product["sizes"] = sizes
    return product
