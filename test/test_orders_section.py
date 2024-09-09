import pytest
import allure
from pages import OrderPage

# Тестовые данные для параметризации
order_test_data = [
    {"name": "Иван", "surname": "Иванов", "address": "Ленинградская, 12", "metro_station": "Бульвар Рокоссовского",
     "phone": "89991112233", "date": "07.09.2024", "rental_period": "трое суток", "color": "black", "comment": "Без звонка"},
    {"name": "Анна", "surname": "Петрова", "address": "Московская, 15", "metro_station": "Чистые пруды",
     "phone": "89991114455", "date": "08.09.2024", "rental_period": "четверо суток", "color": "grey", "comment": "Курьер звонить за час"}
]

# Параметризация теста
@allure.feature("Оформление заказа")
@allure.story("Позитивный сценарий оформления заказа")
@pytest.mark.parametrize("order_data", order_test_data)
def test_order_flow(driver, order_data):
    order_page = OrderPage(driver)

    with allure.step("Нажимаем на кнопку 'Заказать'"):
        order_page.click_order_button()

    with allure.step("Ожидаем загрузки формы заказа"):
        order_page.wait_for_order_form()

    with allure.step(f"Заполняем форму заказа: {order_data['name']} {order_data['surname']}"):
        order_page.fill_order_form(**order_data)

    with allure.step("Подтверждаем заказ"):
        order_page.submit_order()

    with allure.step("Проверяем успешное подтверждение заказа"):
        assert order_page.check_order_confirmation(), "Заказ не был успешно подтвержден!"

