import pytest
import allure
from selenium.webdriver.support.wait import WebDriverWait

from pages import HomePage

@pytest.mark.usefixtures("driver")
class TestLogoRedirects:

    @allure.feature("Проверка логотипа 'Самоката'")
    @allure.description("Тест проверяет, что клик по логотипу 'Самоката' перенаправляет на главную страницу")
    def test_scooter_logo_redirect(self, driver):
        home_page = HomePage(driver)
        home_page.click_scooter_logo()
        assert driver.current_url == 'https://qa-scooter.praktikum-services.ru/', "Не удалось перейти на главную страницу!"

    @allure.feature("Проверка логотипа 'Яндекса'")
    @allure.description("Тест проверяет, что клик по логотипу 'Яндекса' открывает страницу Дзена в новой вкладке")
    def test_yandex_logo_redirect(self, driver):
        home_page = HomePage(driver)
        home_page.click_yandex_logo()
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        assert "dzen.ru" in driver.current_url, "Не удалось открыть страницу Дзена!"
