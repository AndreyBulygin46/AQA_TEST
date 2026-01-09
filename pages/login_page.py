from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object для страницы логина saucedemo.com"""

    # URL страницы
    URL = "https://www.saucedemo.com/"

    # Локаторы элементов
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Открывает страницу логина"""
        self.driver.get(self.URL)
        return self

    def enter_username(self, username):
        """Вводит имя пользователя"""
        username_field = self.wait.until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)
        return self

    def enter_password(self, password):
        """Вводит пароль"""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        return self

    def click_login(self):
        """Нажимает кнопку логина"""
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()
        return self

    def login(self, username, password):
        """Выполняет полный процесс логина"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self):
        """Получает текст сообщения об ошибке"""
        try:
            error_element = self.wait.until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except:
            return None

    def is_error_message_displayed(self):
        """Проверяет, отображается ли сообщение об ошибке"""
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.is_displayed()
        except:
            return False
