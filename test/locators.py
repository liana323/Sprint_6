from selenium.webdriver.common.by import By

class HomePageLocators:
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")

class OrderPageLocators:
    order_button_top = (By.CSS_SELECTOR, ".Header_Nav__AGCXC .Button_Button__ra12g")
    order_button_bottom = (By.CSS_SELECTOR, ".Home_FinishButton__1_cWm .Button_Button__ra12g")
    name_field = (By.XPATH, "//input[@placeholder='* Имя']")
    surname_field = (By.XPATH, "//input[@placeholder='* Фамилия']")
    address_field = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    metro_field = (By.CLASS_NAME, "select-search__input")
    phone_field = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    next_button = (By.XPATH, "//button[contains(text(), 'Далее')]")
    date_field = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    rental_period = (By.CLASS_NAME,"Dropdown-placeholder")
    color_black = (By.ID, "black")
    color_grey = (By.ID, "grey")
    comment_field = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    order_button = (By.XPATH, "//div[contains(@class, 'Order_Buttons__1xGrp')]//button[text()='Заказать']")
    confirm_button = (By.XPATH, "//button[contains(text(), 'Да')]")
    order_confirmation_message = (By.CLASS_NAME, "Order_ModalHeader__3FDaJ")

class QuestionSectionLocators:
    section = (By.CLASS_NAME, "Home_FourPart__1uthg")
    question_sentence = (By.XPATH, '//div[contains(@id, "accordion__heading-")]')
    answer_panel = (By.XPATH, '//div[contains(@id, "accordion__panel-")]')
