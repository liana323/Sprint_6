from selenium.webdriver.common.by import By

from locators import HomePageLocators, OrderPageLocators, QuestionSectionLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def fill_field(self, locator, value, timeout=10):
        field = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(value)

class HomePage(BasePage):
    def click_scooter_logo(self):
        # Клик по логотипу "Самоката"
        self.click_element(HomePageLocators.SCOOTER_LOGO)

    def click_yandex_logo(self):
        # Клик по логотипу Яндекса
        self.click_element(HomePageLocators.YANDEX_LOGO)

        # Ожидаем появления новой вкладки
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Ожидаем загрузки страницы на новой вкладке
        WebDriverWait(self.driver, 10).until(EC.url_contains("dzen.ru"))

class OrderPage(BasePage):
    def click_order_button(self):
        self.click_element(OrderPageLocators.order_button_top)

    def wait_for_order_form(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(OrderPageLocators.name_field))

    def fill_order_form(self, name, surname, address, metro_station, phone, date, rental_period, color, comment):
        # Заполнение имени
        self.fill_field(OrderPageLocators.name_field, name)

        # Заполнение фамилии
        self.fill_field(OrderPageLocators.surname_field, surname)

        # Заполнение адреса
        self.fill_field(OrderPageLocators.address_field, address)

        # Ввод станции метро
        metro_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(OrderPageLocators.metro_field)
        )
        metro_input.click()
        metro_input.send_keys(metro_station)

        # Выбор станции метро из выпадающего списка
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{metro_station}')]"))).click()

        # Заполнение телефона
        self.fill_field(OrderPageLocators.phone_field, phone)

        # Клик на кнопку "Далее"
        self.click_element(OrderPageLocators.next_button)

        # Клик по полю с датой
        self.click_element(OrderPageLocators.date_field)

        # Ожидание и выбор даты из календаря
        calendar_date_xpath = f"//div[contains(@aria-label, 'пятница, 6-е сентября 2024 г.')]"
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, calendar_date_xpath))).click()

        # Ввод периода аренды
        self.click_element(OrderPageLocators.rental_period)
        rental_option_xpath = f"//div[contains(@class, 'Dropdown-option') and text()='{rental_period}']"
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, rental_option_xpath))).click()

        # Выбор цвета самоката
        if color == 'black':
            self.click_element(OrderPageLocators.color_black)
        elif color == 'grey':
            self.click_element(OrderPageLocators.color_grey)

        # Заполнение комментария для курьера
        self.fill_field(OrderPageLocators.comment_field, comment)

    def submit_order(self):
        self.click_element(OrderPageLocators.order_button)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(OrderPageLocators.confirm_button)).click()

    def check_order_confirmation(self):
        confirmation_message = WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located(OrderPageLocators.order_confirmation_message))
        return "Заказ оформлен" in confirmation_message.text

class QuestionSection(BasePage):
    def scroll_to_section(self):
        section_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(QuestionSectionLocators.section))
        self.driver.execute_script("arguments[0].scrollIntoView();", section_element)

    def click_question(self, index):
        self.click_element((By.ID, f"accordion__heading-{index}"))

    def get_answer_text(self, index):
        answer_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, f"accordion__panel-{index}")))
        return answer_element.text
