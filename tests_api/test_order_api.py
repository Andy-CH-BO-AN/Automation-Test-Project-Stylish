import json
import os
from copy import deepcopy

import pytest

from api_objects.create_order_api import CreateOrderApi
from api_objects.get_order_api import GetOrderApi
from api_objects.get_order_prime_api import GetOrderPrimeApi


ORDER_TEMPLATE = {
    "prime": "",
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
            "time": "",
        },
        "list": [
            {
                "color": {"code": "FFFFFF", "name": "白色"},
                "id": "314562783901",
                "image": "http://abc.com/assets/3456789/main.jpg",
                "name": "洋裝",
                "price": 599,
                "qty": 3,
                "size": "S",
            }
        ],
    },
}


@pytest.fixture(params=["anytime", "morning", "afternoon"])
def delivery_time(request):
    return request.param


@pytest.fixture()
def order_info():
    return deepcopy(ORDER_TEMPLATE)


def get_prime(session):
    required_vars = (
        "TAPPAY_TEST_CARD_NUM",
        "TAPPAY_TEST_CARD_DUE_DATE",
        "TAPPAY_TEST_CARD_CCV",
    )
    card_data = {name: os.getenv(name) for name in required_vars}
    missing = [name for name, value in card_data.items() if not value]
    if missing:
        pytest.skip(f"Missing TapPay sandbox config: {', '.join(missing)}")

    response = GetOrderPrimeApi(
        session,
        cardnumber=card_data["TAPPAY_TEST_CARD_NUM"],
        cardduedate=card_data["TAPPAY_TEST_CARD_DUE_DATE"],
        cardccv=card_data["TAPPAY_TEST_CARD_CCV"],
    ).send()
    return json.loads(response.text)["card"]["prime"]


class TestOrderApi:
    def test_user_can_checkout(self, delivery_time, order_info, login, session):
        order_info["prime"] = get_prime(session)
        order_info["order"]["recipient"]["time"] = delivery_time

        response = CreateOrderApi(session, order_info).send()
        assert response.status_code == 200
        order_number = response.json()["data"]["number"]

        response = GetOrderApi(session, order_number).send()
        assert response.status_code == 200
        assert order_info["order"] == response.json()["data"]["details"]

    def test_user_cannot_checkout_with_invalid_prime(self, delivery_time, order_info, login, session):
        order_info["prime"] = f"{get_prime(session)}a"
        order_info["order"]["recipient"]["time"] = delivery_time

        response = CreateOrderApi(session, order_info).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Prime is invalid."

    def test_user_cannot_checkout_without_prime(self, delivery_time, order_info, login, session):
        order_info["order"]["recipient"]["time"] = delivery_time

        response = CreateOrderApi(session, order_info).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Prime is required."

    def test_user_cannot_checkout_with_invalid_order_info(self, login, session):
        response = CreateOrderApi(session, "OvO").send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Order info is invalid"

    def test_user_cannot_checkout_without_order_info(self, login, session):
        response = CreateOrderApi(session, "").send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Order info is required."

    def test_user_cannot_get_order_detail_with_invalid_order_number(
        self, delivery_time, order_info, login, session
    ):
        order_info["prime"] = get_prime(session)
        order_info["order"]["recipient"]["time"] = delivery_time

        response = CreateOrderApi(session, order_info).send()
        assert response.status_code == 200
        invalid_order_number = f"{response.json()['data']['number']}a"

        response = GetOrderApi(session, invalid_order_number).send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Order number is invalid"

    def test_user_cannot_get_order_detail_without_order_number(self, login, session):
        response = GetOrderApi(session, "").send()
        assert response.status_code == 400
        assert response.json()["errorMsg"] == "Order number is required."
