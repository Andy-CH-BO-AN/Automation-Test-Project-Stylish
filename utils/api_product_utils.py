import logging
import os

from api_objects.products_category_api import ProductsCategoryApi
from api_objects.products_search_api import ProductsSearchApi
from table_object.color_table import search_color_code_and_name
from table_object.image_table import search_images_by_product_id
from table_object.variant_table import search_variants_by_product_id


def get_all_pages_products(product_details, pages, session, keyword=None, category=None):
    if keyword is not None and category is not None:
        logging.info("The variables keyword and category cannot coexist simultaneously.")
        assert False

    for paging in range(pages):
        if keyword is not None:
            product_search_api = ProductsSearchApi(session, keyword, paging)
            response = product_search_api.send()
            product_detail_data = response.json()["data"]

        else:
            product_search_api = ProductsCategoryApi(session, category, paging)
            response = product_search_api.send()
            product_detail_data = response.json()["data"]

        product_details += product_detail_data
        assert response.status_code == 200
        if paging < pages - 1:
            logging.info(f"paging: {paging} pages: {pages}")
            assert response.json()["next_paging"] == paging + 1

    return product_details


def processing_data_to_compare_product_detail(db_product_detail, conn):
    colors = []
    sizes = []
    images = []
    db_images_details = search_images_by_product_id(db_product_detail["id"], conn)
    db_variant_details = search_variants_by_product_id(db_product_detail["id"], conn)

    main_image = db_product_detail["main_image"]
    db_product_detail["main_image"] = \
        f"{os.getenv('DOMAIN')}/assets/{db_product_detail['id']}/{main_image}"

    for db_image_detail in db_images_details:
        images.append(
            f"{(os.getenv('DOMAIN'))}/assets/{db_product_detail['id']}/{db_image_detail['image']}")

    for db_variant_detail in db_variant_details:
        color_id = db_variant_detail["color_id"]
        db_variant_detail["color_code"] = search_color_code_and_name(color_id, conn)["code"]
        del db_variant_detail["color_id"]

        color = search_color_code_and_name(color_id, conn)

        if color not in colors:
            colors.append(color)

        if db_variant_detail["size"] not in sizes:
            sizes.append(db_variant_detail["size"])

    db_product_detail["images"] = images
    db_product_detail["variants"] = db_variant_details
    db_product_detail["colors"] = colors
    db_product_detail["sizes"] = sizes

    return db_product_detail
