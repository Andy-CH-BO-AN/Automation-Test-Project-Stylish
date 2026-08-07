from table_object.color_table import search_color
from test_data import test_data_from_excel
import allure
import pytest
from api_objects.create_product_api import CreateProductApi
from api_objects.delete_product_api import DeleteProductApi
from api_objects.products_search_api import ProductsSearchApi
from api_objects.products_detail_api import ProductsDetailApi
from api_objects.logout_api import LogoutApi


@allure.feature("Create and delete product")
class TestCreateProduct:
    @pytest.mark.parametrize('product_info',
                             test_data_from_excel.read_data('test_data/Stylish_TestCase.xlsx',
                                                            'API Create Product Success'))
    @allure.title("admin can create and delete product success")
    def test_admin_can_create_and_delete_product(self, login, session, product_info, setup_db, request):
        keyword = 'm'
        paging = 0

        product_info = {
            'category': product_info['Category'],
            'title': product_info['Title'],
            'description': product_info['Description'],
            'price': product_info['Price'],
            'texture': product_info['Texture'],
            'wash': product_info['Wash'],
            'place': product_info['Place of Product'],
            'note': product_info['Note'],
            'color_ids': product_info['ColorIDs'],
            'sizes': product_info['Sizes'],
            'story': product_info['Story'],
            'main_image': product_info['Main Image'],
            'other_images': [product_info['Other Image 1'], product_info['Other Image 2']]
        }
        create_product_api = CreateProductApi(session, product_info)
        response = create_product_api.send()
        assert response.status_code == 200

        color_ids = product_info['ColorIDs'].split(",")
        for color in range(len(color_ids)):
            color_ids[color] = search_color(color_ids[color], setup_db)

        sizes = product_info['sizes'].split(",")

        product_search_api = ProductsSearchApi(session, keyword, paging)
        response = product_search_api.send()
        product_detail_data = response.json()[0]["data"]

        product_detail_colors = []
        product_detail_sizes = []

        assert product_detail_data['Category'] == product_info['Category']
        assert product_detail_data['title'] == product_info['Title']
        assert product_detail_data['Description'] == product_info['Description']
        assert product_detail_data['Price'] == product_info['Price']
        assert product_detail_data['Texture'] == product_info['Texture']
        assert product_detail_data['Wash'] == product_info['Wash']
        assert product_detail_data['Place of Product'] == product_info['Place of Product']
        assert product_detail_data['Note'] == product_info['Note']
        assert product_detail_data['main_image'] == product_info['main_image']
        assert product_detail_data['other_images'] == product_info['other_images']
        assert product_detail_data['story'] == product_info['story']

        for variant in product_detail_data['variants']:
            if variant["color_code"] not in product_detail_colors:
                product_detail_colors.append(variant["color_code"])
        assert product_detail_colors == color_ids

        for variant in product_detail_data['variants']:
            if variant["size"] not in product_detail_sizes:
                product_detail_sizes.append(variant["size"])
        assert product_detail_sizes == sizes

        product_id = product_detail_data['product_id']
        delete_product_api = DeleteProductApi(session, product_id)
        response = delete_product_api.send()

        assert response.status_code == 200

        product_search_api = ProductsDetailApi(session, product_id)
        response = product_search_api.send()

        assert response.status_code == 404

        def teardown_method():
            product_search_api = ProductsSearchApi(session, keyword, paging)
            response = product_search_api.send()
            if len(response.json()) > 0:
                product_detail_data = response.json()[0]["data"]
                product_id = product_detail_data['product_id']
                delete_product_api = DeleteProductApi(session, product_id)
                delete_product_api.send()
        request.addfinalizer(teardown_method)

    @pytest.mark.parametrize('product_info',
                             test_data_from_excel.read_data('test_data/Stylish_TestCase.xlsx',
                                                            'API Create Product Failed'))
    def test_admin_cannot_create_product_with_invalid_value(self, login, session, product_info, request):
        self.product_info = product_info
        product_info = {
            'category': product_info['Category'],
            'title': product_info['Title'],
            'description': product_info['Description'],
            'price': product_info['Price'],
            'texture': product_info['Texture'],
            'wash': product_info['Wash'],
            'place': product_info['Place of Product'],
            'note': product_info['Note'],
            'color_ids': product_info['ColorIDs'],
            'sizes': product_info['Sizes'],
            'story': product_info['Story'],
            'main_image': product_info['Main Image'],
            'other_images': [product_info['Other Image 1'], product_info['Other Image 2']]
        }
        create_product_api = CreateProductApi(session, product_info)
        response = create_product_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == self.product_info['Error Msg']

        def teardown_method():
            keyword = 'm'
            paging = 0
            product_search_api = ProductsSearchApi(session, keyword, paging)
            response = product_search_api.send()
            if len(response.json()) > 0:
                product_detail_data = response.json()[0]["data"]
                product_id = product_detail_data['product_id']
                delete_product_api = DeleteProductApi(session, product_id)
                delete_product_api.send()
        request.addfinalizer(teardown_method)

    def test_admin_cannot_create_product_without_login(self, session, request):
        product_info = {
            'category': 'men',
            'title': 'm',
            'description': 'm',
            'price': 69,
            'texture': 'm',
            'wash': 'm',
            'place': 'm',
            'note': 'm',
            'color_ids': ['1', '2'],
            'sizes': ['M', 'XL'],
            'story': 'm',
            'main_image': 'mainImage.jpg',
            'other_images': ['otherImage0.jpg', 'otherImage1.jpg']
        }
        create_product_api = CreateProductApi(session, product_info)
        response = create_product_api.send()
        assert response.status_code == 401
        assert response.json()['errorMsg'] == 'Unauthorized'

        def teardown_method():
            keyword = 'm'
            paging = 0
            product_search_api = ProductsSearchApi(session, keyword, paging)
            response = product_search_api.send()
            if len(response.json()) > 0:
                product_detail_data = response.json()[0]["data"]
                product_id = product_detail_data['product_id']
                delete_product_api = DeleteProductApi(session, product_id)
                delete_product_api.send()
        request.addfinalizer(teardown_method)

    def test_admin_cannot_delete_product_without_login(self, login, session, setup_db, request):
        keyword = 'm'
        paging = 0

        product_info = {
            'category': 'men',
            'title': 'm',
            'description': 'm',
            'price': 69,
            'texture': 'm',
            'wash': 'm',
            'place': 'm',
            'note': 'm',
            'color_ids': ['1', '2'],
            'sizes': ['M', 'XL'],
            'story': 'm',
            'main_image': 'mainImage.jpg',
            'other_images': ['otherImage0.jpg', 'otherImage1.jpg']
        }
        create_product_api = CreateProductApi(session, product_info)
        response = create_product_api.send()
        assert response.status_code == 200

        product_search_api = ProductsSearchApi(session, keyword, paging)
        response = product_search_api.send()
        product_detail_data = response.json()[0]["data"]
        product_id = product_detail_data['product_id']

        logout_api = LogoutApi(session)
        logout_api.send()

        delete_product_api = DeleteProductApi(session, product_id)
        response = delete_product_api.send()
        assert response.status_code == 401
        assert response.json()['errorMsg'] == 'Unauthorized'

        def teardown_method():
            keyword = 'm'
            paging = 0
            product_search_api = ProductsSearchApi(session, keyword, paging)
            response = product_search_api.send()
            if len(response.json()) > 0:
                product_detail_data = response.json()[0]["data"]
                product_id = product_detail_data['product_id']
                delete_product_api = DeleteProductApi(session, product_id)
                delete_product_api.send()
        request.addfinalizer(teardown_method)

    def test_admin_cannot_delete_product_without_product_id(self, login, session):
        product_id = ""
        delete_product_api = DeleteProductApi(session, product_id)
        response = delete_product_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Product ID not found.'

    def test_admin_cannot_delete_product_with_product_id_not_exist(self, login, session):
        product_id = 123412341234
        delete_product_api = DeleteProductApi(session, product_id)
        response = delete_product_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Product ID not found.'

    def test_admin_cannot_delete_product_with_invalid_product_id(self, login, session):
        product_id = "a"
        delete_product_api = DeleteProductApi(session, product_id)
        response = delete_product_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Invalid Product ID'
