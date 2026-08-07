import json
import logging
import os

import allure
import pytest
from api_objects.create_order_api import CreateOrderApi
from api_objects.get_order_prime_api import GetOrderPrimeApi
from api_objects.get_order_api import GetOrderApi


class TestOrderApi:
    test_card_num = "4242424242424242"
    test_card_due_date = "202404"
    test_card_ccv = "424"

    order_info = {
        "prime": '',

        "order": {
            "shipping": "delivery",
            "payment": "credit_card",
            "subtotal": 1797,
            "freight": 30,
            "total": 1827,

            "recipient": {
                "name": "mane",
                "phone": "0809000550",
                "email": "aaa@bbb.com",
                "address": "台北市中正區重慶南路一段122號",
                "time": ""
            },

            "list": [{
                "color": {
                    "code": "FFFFFF",
                    "name": "白色"
                },
                "id": "314562783901",
                "image": "http://abc.com/assets/3456789/main.jpg",
                "name": "洋裝",
                "price": 599,
                "qty": 3,
                "size": "S"
            }]
        }
    }

    @pytest.mark.parametrize(argnames="time",
                             argvalues=["anytime", "morning", "afternoon"])
    def test_user_can_checkout(self, time, login, session):
        get_prime_api = GetOrderPrimeApi(session, cardnumber=self.test_card_num, cardduedate=self.test_card_due_date,
                                         cardccv=self.test_card_ccv)
        response = get_prime_api.send()
        prime = json.loads(response.text)["card"]["prime"]
        self.order_info["prime"] = prime
        self.order_info["order"]["recipient"]["time"] = time

        create_order_api = CreateOrderApi(session, self.order_info)
        response = create_order_api.send()
        order_number = response.json()['data']['number']

        get_order_api = GetOrderApi(session, order_number)
        response = get_order_api.send()
        order_detail = response.json()
        order_detail["data"]["number"] = order_number
        assert self.order_info["order"] == order_detail["data"]["details"], \
            logging.info(f"self.order_info['order']: {self.order_info['order']} "
                         f"order_detail['data']['details']: {order_detail['data']['details']}")

    def test_user_cannot_checkout_with_invalid_prime(self, time, login, session):
        get_prime_api = GetOrderPrimeApi(session, cardnumber=self.test_card_num, cardduedate=self.test_card_due_date,
                                         cardccv=self.test_card_ccv)
        response = get_prime_api.send()
        prime = f"{json.loads(response.text)['card']['prime']}a"
        order_info = self.order_info
        order_info["prime"] = prime
        order_info["order"]["recipient"]["time"] = time

        create_order_api = CreateOrderApi(session, order_info)
        response = create_order_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Prime is invalid.'

    def test_user_cannot_checkout_without_prime(self, time, login, session):
        get_prime_api = GetOrderPrimeApi(session, cardnumber=self.test_card_num, cardduedate=self.test_card_due_date,
                                         cardccv=self.test_card_ccv)
        get_prime_api.send()
        self.order_info["order"]["recipient"]["time"] = time

        create_order_api = CreateOrderApi(session, self.order_info)
        response = create_order_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Prime is required.'

    def test_user_cannot_checkout_with_invalid_order_info(self, login, session):
        get_prime_api = GetOrderPrimeApi(session, cardnumber=self.test_card_num, cardduedate=self.test_card_due_date,
                                         cardccv=self.test_card_ccv)
        get_prime_api.send()
        order_info = "OvO"

        create_order_api = CreateOrderApi(session, order_info)
        response = create_order_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Order info is invalid'

    def test_user_cannot_checkout_without_order_info(self, login, session):
        get_prime_api = GetOrderPrimeApi(session, cardnumber=self.test_card_num, cardduedate=self.test_card_due_date,
                                         cardccv=self.test_card_ccv)
        get_prime_api.send()
        order_info = ''
        create_order_api = CreateOrderApi(session, order_info)
        response = create_order_api.send()
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Order info is required.'

    def test_user_cannot_get_order_detail_with_invalid_order_number(self, time, login, session):
        get_prime_api = GetOrderPrimeApi(session, cardnumber=self.test_card_num, cardduedate=self.test_card_due_date,
                                         cardccv=self.test_card_ccv)
        response = get_prime_api.send()
        prime = json.loads(response.text)["card"]["prime"]
        self.order_info["prime"] = prime
        self.order_info["order"]["recipient"]["time"] = time

        create_order_api = CreateOrderApi(session, self.order_info)
        response = create_order_api.send()
        order_number = f"{response.json()['data']['number']}a"

        get_order_api = GetOrderApi(session, order_number)
        response = get_order_api.send()
        order_detail = response.json()
        order_detail["data"]["number"] = order_number
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Order number is invalid'

    def test_user_cannot_get_order_detail_without_order_number(self, login, session):
        order_number = ""
        get_order_api = GetOrderApi(session, order_number)
        response = get_order_api.send()
        order_detail = response.json()
        order_detail["data"]["number"] = order_number
        assert response.status_code == 400
        assert response.json()['errorMsg'] == 'Order number is required.'
