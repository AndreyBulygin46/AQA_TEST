from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductsPage:
    """Page Object для страницы с продуктами после успешного логина"""

    # URL страницы продуктов
    URL = "https://www.saucedemo.com/inventory.html"

    # Локаторы элементов
    PRODUCTS_TITLE = (By.CSS_SELECTOR, ".title")
    PRODUCTS_CONTAINER = (By.CSS_SELECTOR, "#inventory_container")
    SHOPPING_CART = (By.CSS_SELECTOR, ".shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self):
        """Проверяет, загрузилась ли страница продуктов"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.PRODUCTS_TITLE)
            )
            return True
        except:
            return False

    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url

    def is_products_title_displayed(self):
        """Проверяет, отображается ли заголовок 'Products'"""
        try:
            title = self.driver.find_element(*self.PRODUCTS_TITLE)
            return title.is_displayed() and "Products" in title.text
        except:
            return False

    def is_products_container_displayed(self):
        """Проверяет, отображается ли контейнер с продуктами"""
        try:
            container = self.driver.find_element(*self.PRODUCTS_CONTAINER)
            return container.is_displayed()
        except:
            return False

    def is_shopping_cart_displayed(self):
        """Проверяет, отображается ли корзина"""
        try:
            cart = self.driver.find_element(*self.SHOPPING_CART)
            return cart.is_displayed()
        except:
            return False
