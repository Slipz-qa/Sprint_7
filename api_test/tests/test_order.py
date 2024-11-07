import pytest
import requests
from api_test.data import BASE_URL, ORDERS_URL

class TestOrderCreation:
    @pytest.mark.parametrize("color", ["BLACK", "GREY"])
    def test_create_order(self, create_order):
        response_data = create_order
        assert "track" in response_data, "Ответ не содержит track."

    @pytest.mark.parametrize("colors", [
        (["BLACK", "GREY"]),
        (["BLACK"]),
        (["GREY"]),
        ([])
    ])
    def test_create_order_with_optional_colors(self, order_data, colors):
        payload = {**order_data}
        if colors:
            payload["color"] = colors

        response = requests.post(f'{BASE_URL}{ORDERS_URL}', json=payload)

        assert response.status_code == 201, f"Ошибка при создании заказа: {response.json()}"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track."
