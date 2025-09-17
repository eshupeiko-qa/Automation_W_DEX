#pytest tests\UI\tests_swap.py --driver Chrome --driver-path D:\chromedriver-win64\chromedriver.exe
# tests/pages/swap_page.py
#pytest tests\UI\tests_swap.py --alluredir=allure-results
# tests/test_swap.py
import pytest
from tests.pages.swap_page import SwapPage
import allure
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.ui
@allure.epic("Swap Page")
@allure.feature("UI Tests")
class TestSwapPage:

    @allure.story("Page Load")
    @allure.title("Проверка загрузки страницы Swap")
    def test_page_loads(self, driver):
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)
        page.wait_for_page_load()

        assert "/swap" in driver.current_url
        assert page.get_from_token() == "POL"
        assert page.get_to_token() == "USDT"

    @allure.story("Input")
    @allure.title("Ввод суммы в поле POL")
    def test_enter_amount_in_pol(self, driver):
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)

        page.enter_amount_pol(5)

        value = page.get_input_value_pol()
        assert float(value) == 5.0

    @allure.story("Max Button")
    @allure.title("Работа кнопки Max для POL")
    def test_max_button_works(self, driver):
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)

        balance = page.get_balance_pol()
        page.click_max_pol()

        entered_value = float(page.get_input_value_pol())
        assert entered_value == balance

    @allure.story("Inversion")
    @allure.title("Кнопка инверсии меняет направление обмена")
    def test_invert_tokens(self, driver):
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)

        from_before = page.get_from_token()
        to_before = page.get_to_token()
        assert from_before == "POL"
        assert to_before == "USDT"

        page.enter_amount_pol(3.5)
        original_value = page.get_input_value_pol()

        page.click_invert()

        from_after = page.get_from_token()
        to_after = page.get_to_token()

        assert from_after == "USDT"
        assert to_after == "POL"

        new_value = page.get_input_value_usdt()
        assert new_value == original_value

    @allure.story("Swap Button")
    @allure.title("Кнопка Swap становится активной после ввода")
    def test_swap_button_enables(self, driver):
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)

        page.enter_amount_pol(1)

        assert page.is_swap_button_enabled(), "Кнопка Swap должна стать активной"

    @allure.story("Navigation")
    @allure.title("Переход на вкладку Pools")
    def test_navigate_to_pools(self, driver):
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)

        page.navigate_to_pools()

        self.wait = WebDriverWait(driver, 10)
        self.wait.until(lambda d: "/pools" in d.current_url)
        assert "/pools" in driver.current_url

    @allure.story("Web3 Integration")
    @allure.title("Проверка Web3 компонентов на странице Swap")
    def test_web3_components_on_swap(self, driver):
        """Проверяет наличие и функциональность Web3 компонентов"""
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)
        page.wait_for_page_load()
        
        # Проверяем логотип DEX
        assert page.is_logo_visible(), "Логотип DEX должен быть виден на странице swap"
        
        # Проверяем кнопку сети
        assert page.is_network_button_visible(), "Кнопка сети должна быть видна"
        network_name = page.get_network_name()
        assert network_name is not None, "Название сети должно отображаться"
        assert "Polygon" in network_name, "Должна отображаться сеть Polygon"

    @allure.story("Web3 Integration") 
    @allure.title("Проверка подключенного аккаунта на Swap")
    def test_connected_account_on_swap(self, driver):
        """Проверяет отображение данных подключенного аккаунта на swap странице"""
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)
        page.wait_for_page_load()
        
        if page.is_account_connected():
            # Если аккаунт подключен, проверяем его данные
            balance = page.get_account_balance()
            address = page.get_account_address()
            
            assert balance is not None, "Баланс аккаунта должен отображаться в Web3 кнопке"
            assert "POL" in balance, "В балансе должны быть токены POL"
            assert address is not None, "Адрес аккаунта должен отображаться"
            assert address.startswith("0x"), "Адрес должен начинаться с 0x"
            assert len(address) == 42, "Адрес должен содержать 42 символа"

    @allure.story("Page Structure")
    @allure.title("Проверка структуры Swap страницы")
    def test_swap_page_structure(self, driver):
        """Проверяет основную структуру и элементы swap страницы"""
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)
        page.wait_for_page_load()
        
        # Проверяем основные элементы структуры
        assert page.is_logo_visible(), "Логотип должен быть виден"
        assert page.is_network_button_visible(), "Кнопка сети должна быть видна"
        
        # Проверяем наличие Web3 модала
        assert page.is_w3m_modal_present(), "Web3 модал должен присутствовать на странице"
        
        # Проверяем, что страница имеет правильный CSS класс
        body_class = driver.find_element("tag name", "body").get_attribute("class")
        assert "metaforce-blue" in body_class, "Body должен иметь класс metaforce-blue"

    @allure.story("Responsive Design")
    @allure.title("Проверка адаптивности интерфейса Swap")
    def test_swap_responsive_design(self, driver):
        """Проверяет адаптивность интерфейса swap страницы для разных размеров экрана"""
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)
        page.wait_for_page_load()
        
        # Тестируем десктопный размер
        driver.set_window_size(1200, 800)
        page.wait_for_page_load()
        
        desktop_wallet_visible = page.is_desktop_wallet_area_visible()
        mobile_menu_visible = page.is_mobile_menu_visible()
        
        # На десктопе должна быть видна область кошелька, но не мобильное меню
        assert desktop_wallet_visible or not mobile_menu_visible, "На десктопе должен отображаться правильный интерфейс"

    @allure.story("Navigation")
    @allure.title("Проверка навигации через логотип со Swap страницы")
    def test_logo_navigation_from_swap(self, driver):
        """Проверяет, что клик по логотипу с swap страницы ведет на главную"""
        driver.get("https://w-dex.ai/swap")
        page = SwapPage(driver)
        page.wait_for_page_load()
        
        # Убеждаемся, что находимся на swap странице
        assert "/swap" in driver.current_url, "Должны находиться на swap странице"
        
        # Кликаем по логотипу
        page.click_logo()
        
        # Проверяем, что перешли на главную страницу
        WebDriverWait(driver, 10).until(lambda d: "/" in d.current_url.split('/')[-1] or d.current_url.endswith('/'))
        current_url = driver.current_url
        assert current_url.endswith('/') or '/swap' not in current_url, "Клик по логотипу должен вести на главную страницу"