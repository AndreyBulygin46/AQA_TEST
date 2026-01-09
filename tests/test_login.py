import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@allure.feature("Авторизация")
@allure.story("Тесты авторизации на saucedemo.com")
class TestLogin:
    """Тесты для проверки функциональности авторизации"""

    @allure.title("Тест 1: Успешный логин с валидными данными")
    @allure.description("Проверка успешной авторизации с стандартным пользователем")
    @pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
    def test_successful_login(self, driver, login_page, username, password):
        """
        Тест 1: Успешный логин
        Проверяет, что пользователь может успешно авторизоваться с валидными данными
        """
        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step(f"Ввести логин '{username}' и пароль"):
            login_page.enter_username(username)
            login_page.enter_password(password)

        with allure.step("Нажать кнопку входа"):
            login_page.click_login()

        with allure.step("Проверить переход на страницу продуктов"):
            products_page = ProductsPage(driver)

            # Проверка URL
            assert products_page.get_current_url() == ProductsPage.URL, \
                f"Ожидался URL {ProductsPage.URL}, получен {products_page.get_current_url()}"

            # Проверка загрузки страницы
            assert products_page.is_loaded(), "Страница продуктов не загрузилась"

            # Проверка отображения элементов
            assert products_page.is_products_title_displayed(), \
                "Заголовок 'Products' не отображается"
            assert products_page.is_products_container_displayed(), \
                "Контейнер с продуктами не отображается"
            assert products_page.is_shopping_cart_displayed(), \
                "Корзина покупок не отображается"

    @allure.title("Тест 2: Логин с неверным паролем")
    @allure.description("Проверка отображения ошибки при неверном пароле")
    def test_login_with_wrong_password(self, driver, login_page):
        """
        Тест 2: Логин с неверным паролем
        Проверяет, что при неверном пароле отображается сообщение об ошибке
        """
        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Ввести валидный логин и неверный пароль"):
            login_page.enter_username("standard_user")
            login_page.enter_password("wrong_password")

        with allure.step("Нажать кнопку входа"):
            login_page.click_login()

        with allure.step("Проверить отображение сообщения об ошибке"):
            assert login_page.is_error_message_displayed(), \
                "Сообщение об ошибке не отображается"

            error_message = login_page.get_error_message()
            assert error_message is not None, "Текст сообщения об ошибке отсутствует"
            assert "Username and password do not match" in error_message or \
                   "Epic sadface" in error_message, \
                f"Неожиданное сообщение об ошибке: {error_message}"

            # Проверка, что остались на странице логина
            assert driver.current_url == LoginPage.URL, \
                "Не должны были перейти на другую страницу при ошибке"

    @allure.title("Тест 3: Логин заблокированного пользователя")
    @allure.description("Проверка блокировки пользователя locked_out_user")
    def test_locked_out_user_login(self, driver, login_page):
        """
        Тест 3: Логин заблокированного пользователя
        Проверяет, что заблокированный пользователь не может войти
        """
        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Ввести логин заблокированного пользователя"):
            login_page.enter_username("locked_out_user")
            login_page.enter_password("secret_sauce")

        with allure.step("Нажать кнопку входа"):
            login_page.click_login()

        with allure.step("Проверить отображение сообщения о блокировке"):
            assert login_page.is_error_message_displayed(), \
                "Сообщение об ошибке не отображается"

            error_message = login_page.get_error_message()
            assert error_message is not None, "Текст сообщения об ошибке отсутствует"
            assert "locked out" in error_message.lower() or \
                   "Epic sadface" in error_message, \
                f"Неожиданное сообщение об ошибке: {error_message}"

            # Проверка, что остались на странице логина
            assert driver.current_url == LoginPage.URL, \
                "Не должны были перейти на другую страницу при ошибке"

    @allure.title("Тест 4: Логин с пустыми полями")
    @allure.description("Проверка валидации пустых полей")
    def test_login_with_empty_fields(self, driver, login_page):
        """
        Тест 4: Логин с пустыми полями
        Проверяет, что при пустых полях отображается сообщение об ошибке
        """
        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Попытаться войти без заполнения полей"):
            login_page.click_login()

        with allure.step("Проверить отображение сообщения об ошибке"):
            assert login_page.is_error_message_displayed(), \
                "Сообщение об ошибке не отображается"

            error_message = login_page.get_error_message()
            assert error_message is not None, "Текст сообщения об ошибке отсутствует"
            assert "Username is required" in error_message or \
                   "Epic sadface" in error_message, \
                f"Неожиданное сообщение об ошибке: {error_message}"

            # Проверка, что остались на странице логина
            assert driver.current_url == LoginPage.URL, \
                "Не должны были перейти на другую страницу при ошибке"

    @allure.title("Тест 5: Логин пользователем performance_glitch_user")
    @allure.description("Проверка корректного перехода при возможных задержках")
    def test_performance_glitch_user_login(self, driver, login_page):
        """
        Тест 5: Логин пользователем performance_glitch_user
        Проверяет корректный переход на страницу продуктов несмотря на возможные задержки
        """
        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Ввести логин performance_glitch_user"):
            login_page.enter_username("performance_glitch_user")
            login_page.enter_password("secret_sauce")

        with allure.step("Нажать кнопку входа и дождаться загрузки"):
            login_page.click_login()
            
            # Увеличиваем время ожидания для пользователя с задержками
            products_page = ProductsPage(driver)
            # Увеличиваем timeout для этого теста (30 секунд вместо 10)
            products_page.wait = WebDriverWait(driver, 30)

        with allure.step("Проверить переход на страницу продуктов после задержки"):
            # Проверка URL
            assert products_page.get_current_url() == ProductsPage.URL, \
                f"Ожидался URL {ProductsPage.URL}, получен {products_page.get_current_url()}"

            # Проверка загрузки страницы (с увеличенным временем ожидания)
            assert products_page.is_loaded(), \
                "Страница продуктов не загрузилась (возможно, из-за задержки)"

            # Проверка отображения элементов
            assert products_page.is_products_title_displayed(), \
                "Заголовок 'Products' не отображается"
            assert products_page.is_products_container_displayed(), \
                "Контейнер с продуктами не отображается"
            assert products_page.is_shopping_cart_displayed(), \
                "Корзина покупок не отображается"
