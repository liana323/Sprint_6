import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class TestLogoRedirects:
    driver = None

    # Локаторы
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")

    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Firefox()

    @allure.feature("Проверка логотипа 'Самоката'")
    @allure.story("Переход на главную страницу при клике на логотип")
    def test_scooter_logo_redirect(self):
        # Переход на страницу
        self.driver.get('https://qa-scooter.praktikum-services.ru/')

        # Ожидание и клик на логотип "Самокат"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SCOOTER_LOGO)).click()

        # Проверяем, что после клика на логотип мы перешли на главную страницу
        assert self.driver.current_url == 'https://qa-scooter.praktikum-services.ru/', "Не удалось перейти на главную страницу при клике на логотип 'Самокат'!"

    @allure.feature("Проверка логотипа 'Яндекса'")
    @allure.story("Переход на главную страницу Дзена в новой вкладке")
    def test_yandex_logo_redirect(self):
        # Переход на страницу
        self.driver.get('https://qa-scooter.praktikum-services.ru/')

        # Ожидание и клик на логотип Яндекса
        yandex_logo = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.YANDEX_LOGO))
        yandex_logo.click()  # Клик по логотипу Яндекса

        # Переключаемся на новую вкладку
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Ожидаем загрузки страницы
        WebDriverWait(self.driver, 10).until(EC.any_of(EC.url_contains("dzen.ru")))

        # Проверяем, что URL ведет либо на авторизацию, либо на главную страницу Дзена
        current_url = self.driver.current_url
        assert "dzen.ru" in current_url,"Не удалось открыть страницу Дзена"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
