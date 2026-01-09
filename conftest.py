import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для создания и закрытия драйвера браузера
    scope="function" означает, что для каждого теста создается новый браузер
    """
    # Настройки Chrome
    chrome_options = Options()
    # Автоматически включаем headless режим в Docker, для локального запуска можно отключить
    if os.environ.get('DOCKER_ENV') == 'true' or os.path.exists('/.dockerenv'):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")

    # Создание драйвера
    # Используем ChromeDriverManager для автоматической установки драйвера
    driver_executable = "chromedriver.exe" if os.name == "nt" else "chromedriver"
    
    try:
        driver_path = ChromeDriverManager().install()
        
        # Ищем правильный файл chromedriver
        found_driver = None
        
        if os.path.isdir(driver_path):
            # Если возвращена директория, ищем chromedriver внутри
            for root, _, files in os.walk(driver_path):
                # Сначала ищем точное совпадение
                if driver_executable in files:
                    potential = os.path.join(root, driver_executable)
                    if os.name == "nt" or os.access(potential, os.X_OK):
                        found_driver = potential
                        break
                
                # Ищем файл chromedriver (без расширения для Linux)
                # Исключаем все файлы, которые явно не являются исполняемым драйвером
                excluded_patterns = ('THIRD_PARTY', 'LICENSE', 'NOTICE', 'NOTICES', 
                                     '.txt', '.md', '.license', '.notice', '.chromedriver')
                for file in files:
                    # Игнорируем файлы с исключенными паттернами
                    if any(pattern in file.upper() for pattern in excluded_patterns):
                        continue
                    
                    # Ищем файл, который называется chromedriver или начинается с chromedriver
                    if file == driver_executable or file == "chromedriver":
                        potential_driver = os.path.join(root, file)
                        # Проверяем, что это исполняемый файл (для Linux) или просто файл (для Windows)
                        if os.path.isfile(potential_driver):
                            if os.name == "nt" or os.access(potential_driver, os.X_OK):
                                found_driver = potential_driver
                                break
                
                if found_driver:
                    break
        elif os.path.isfile(driver_path):
            # Проверяем, что это правильный файл и не является документом
            if "THIRD_PARTY" not in driver_path.upper() and "LICENSE" not in driver_path.upper() and "NOTICE" not in driver_path.upper():
                if driver_path.endswith(driver_executable):
                    found_driver = driver_path
                elif os.name != "nt" and driver_path.endswith('chromedriver') and os.access(driver_path, os.X_OK):
                    found_driver = driver_path
            
            # Если не нашли правильный файл, ищем в той же директории
            if not found_driver:
                dir_name = os.path.dirname(driver_path)
                if os.path.isdir(dir_name):
                    excluded_patterns = ('THIRD_PARTY', 'LICENSE', 'NOTICE', 'NOTICES', 
                                         '.txt', '.md', '.license', '.notice', '.chromedriver')
                    for file in os.listdir(dir_name):
                        # Пропускаем файлы с исключенными паттернами
                        if any(pattern in file.upper() for pattern in excluded_patterns):
                            continue
                        
                        potential_path = os.path.join(dir_name, file)
                        if (file == driver_executable or file == "chromedriver") and os.path.isfile(potential_path):
                            if os.name == "nt" or os.access(potential_path, os.X_OK):
                                found_driver = potential_path
                                break
        
        # Используем найденный драйвер или Service() без пути
        if found_driver and os.path.isfile(found_driver):
            service = Service(found_driver)
        else:
            # Fallback: используем Service() без пути - Selenium найдет драйвер через PATH
            service = Service()
    except Exception:
        # Если что-то пошло не так, используем Service() без пути
        service = Service()

    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver  # Передаем драйвер в тест

    # Закрываем браузер после теста
    driver.quit()


@pytest.fixture
def login_page(driver):
    """
    Фикстура для создания объекта страницы логина
    """
    return LoginPage(driver)
