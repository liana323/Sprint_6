from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest

# Page Object для выпадающего списка в разделе "Вопросы о важном"
class QuestionSection:
    def __init__(self, driver):
        self.driver = driver

    # Локаторы для секции "Вопросы о важном"

    section = (By.CLASS_NAME, "Home_FourPart__1uthg")
    question_sentence = (By.XPATH, '//div[contains(@id, "accordion__heading-")]')
    answer_panel = (By.XPATH, '//div[contains(@id, "accordion__panel-")]')

    @allure.step("Прокрутка к разделу 'Вопросы о важном'")
    def scroll_to_section(self):
        section_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.section)
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", section_element)

    @allure.step("Клик по вопросу")
    def click_question(self, index):
        question_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"accordion__heading-{index}"))
        )
        question_element.click()

    @allure.step("Получение текста ответа")
    def get_answer_text(self, index):
        answer_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, f"accordion__panel-{index}"))
        )
        return answer_element.text

# Автотесты для "Вопросы о важном"
class TestSection:
    driver = None

    @classmethod
    def setup_class(cls):
        # Создаем драйвер для браузера Firefox
        cls.driver = webdriver.Firefox()

    @allure.feature("Проверка раздела 'Вопросы о важном'")
    @allure.story("Проверка вопросов и ответов")
    def test_question_answer(self):
        # Переход на страницу
        self.driver.get('https://qa-scooter.praktikum-services.ru/')

        # Создаем объект класса QuestionSection
        questions_section = QuestionSection(self.driver)

        # Прокручиваем до раздела "Вопросы о важном"
        questions_section.scroll_to_section()

        # Параметры для вопросов и ожидаемых ответов
        questions_and_answers = [
            (0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой."),
            (1, "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим."),
            (2, "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30."),
            (3, "Только начиная с завтрашнего дня. Но скоро станем расторопнее."),
            (4, "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010."),
            (5, "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится."),
            (6, "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои."),
            (7, "Да, обязательно. Всем самокатов! И Москве, и Московской области.")
        ]

        # Проверяем каждый вопрос
        for index, expected_answer in questions_and_answers:
            questions_section.click_question(index)
            answer_text = questions_section.get_answer_text(index)
            assert expected_answer in answer_text, f"Ответ для вопроса {index} не совпадает!"

    @classmethod
    def teardown_class(cls):
        # Закрываем браузер
        cls.driver.quit()
