import pytest
import allure

from page_objects.index_page import IndexPage

women_list = ["前開衩扭結洋裝", "透肌澎澎防曬襯衫", "小扇紋細織上衣", "活力花紋長筒牛仔褲", "精緻扭結洋裝",
              "透肌澎澎薄紗襯衫", "小扇紋質感上衣", "經典修身長筒牛仔褲"]
men_list = ['純色輕薄百搭襯衫', '時尚輕鬆休閒西裝', '經典商務西裝']
accessories_list = ['夏日海灘戶外遮陽帽', '經典牛仔帽', '卡哇伊多功能隨身包', '柔軟氣質羊毛圍巾']


@pytest.mark.parametrize("category, products_list", [
    ("women", women_list),
    ("men", men_list),
    ("accessories", accessories_list)])
@allure.title(f"categories")
def test_categories(category, products_list, setup_driver):
    index_page = IndexPage(setup_driver)
    index_page.go_to_category(category)
    assert index_page.check_products_name(products_list)
