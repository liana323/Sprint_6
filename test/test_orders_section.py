import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class Orderpage:
    def __init__(self, driver):
        self.driver = driver

    # Локаторы кнопок "Заказать"
    order_button_top = (By.CSS_SELECTOR, ".Header_Nav__AGCXC .Button_Button__ra12g")
    order_button_bottom = (By.CSS_SELECTOR, ".Home_FinishButton__1_cWm .Button_Button__ra12g")

    # Локаторы для полей формы "Для кого самокат"
    name_field = (By.XPATH, "//input[@placeholder='* Имя']")
    surname_field = (By.XPATH, "//input[@placeholder='* Фамилия']")
    address_field = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    metro_field = (By.CLASS_NAME, "select-search__input")
    phone_field = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    next_button = (By.XPATH, "//button[contains(text(), 'Далее')]")

    # Локаторы для полей формы "Про аренду"
    date_field = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    rental_period = (By.CLASS_NAME,"Dropdown-placeholder")
    color_black = (By.ID, "black")
    color_grey = (By.ID, "grey")
    comment_field = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    order_button = (By.XPATH, "//div[contains(@class, 'Order_Buttons__1xGrp')]//button[text()='Заказать']")
    confirm_button = (By.XPATH, "//button[contains(text(), 'Да')]")

    @allure.step("Нажимаем на кнопку 'Заказать'")
    def click_order_button(self):
        self.driver.find_element(*self.order_button_top).click()

    @allure.step("Ожидаем форму заказа")
    def wait_for_order_form(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.name_field)
        )

    @allure.step("Заполняем форму заказа")
    def fill_order_form(self, name, surname, address, metro_station, phone, date, rental_period, color, comment):
        self.driver.find_element(*self.name_field).send_keys(name)
        self.driver.find_element(*self.surname_field).send_keys(surname)
        self.driver.find_element(*self.address_field).send_keys(address)

        metro_input = self.driver.find_element(*self.metro_field)
        metro_input.click()
        metro_input.send_keys(metro_station)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{metro_station}')]"))
        ).click()

        self.driver.find_element(*self.phone_field).send_keys(phone)
        self.driver.find_element(*self.next_button).click()

        #Бесячий календарь
        self.driver.find_element(*self.date_field).click()
        calendar_date_xpath = f"//div[contains(@aria-label, 'пятница, 6-е сентября 2024 г.')]"

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, calendar_date_xpath))).click()

        #срок аренды
        self.driver.find_element(*self.rental_period).click()
        rental_option_xpath = f"//div[contains(@class, 'Dropdown-option') and text()='{rental_period}']"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, rental_option_xpath))).click()

        # Выбираем цвет самоката
        if color == 'black':
            self.driver.find_element(By.ID, "black").click()
        elif color == 'grey':
            self.driver.find_element(By.ID, "grey").click()

        self.driver.find_element(*self.comment_field).send_keys(comment)

    @allure.step("Подтверждаем заказ")
    def submit_order(self):
        # Нажимаем кнопку "Заказать"
        self.driver.find_element(*self.order_button).click()

        # Ожидание появления окна
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "Order_ModalHeader__3FDaJ")))

        # Ожидание и клик на кнопку "Да"
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.confirm_button)
        ).click()

    @allure.step("Проверяем подтверждение заказа")
    def check_order_confirmation(self):
        confirmation_message = WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "Order_ModalHeader__3FDaJ")))
        return "Заказ оформлен" in confirmation_message.text


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.get('https://qa-scooter.praktikum-services.ru/')
    yield driver
    driver.quit()

@pytest.mark.parametrize("order_data", [
    {"name": "Иван", "surname": "Иванов", "address": "Ленинградская, 12", "metro": "Бульвар Рокоссовского",
     "phone": "89991112233", "date": "07.09.2024", "rental_period": "трое суток", "color": "black", "comment": "Без звонка"},
    {"name": "Анна", "surname": "Петрова", "address": "Московская, 15", "metro": "Чистые пруды",
     "phone": "89991114455", "date": "08.09.2024", "rental_period": "четверо суток", "color": "grey", "comment": "Курьер звонить за час"}])

def test_order_flow(driver, order_data):
    order_page = Orderpage(driver)

    # Нажимаем кнопку "Заказать"
    order_page.click_order_button()

    # Ожидаем загрузки формы заказа
    order_page.wait_for_order_form()

    # Заполняем форму заказа
    order_page.fill_order_form(
        name=order_data["name"],
        surname=order_data["surname"],
        address=order_data["address"],
        metro_station=order_data["metro"],
        phone=order_data["phone"],
        date=order_data["date"],
        rental_period=order_data["rental_period"],
        color=order_data["color"],
        comment=order_data["comment"])

    # Подтверждаем заказ
    order_page.submit_order()

    # Проверяем успешное подтверждение заказа
    assert order_page.check_order_confirmation(), "Заказ не был успешно подтвержден!"
