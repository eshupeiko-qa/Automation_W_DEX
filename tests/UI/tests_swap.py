#pytest tests\UI\tests_swap.py --driver Chrome --driver-path D:\chromedriver-win64\chromedriver.exe
# tests/pages/swap_page.py
#pytest tests\UI\tests_swap.py --alluredir=allure-results
# tests/test_swap.py
import pytest
from tests.pages.swap_page import SwapPage
import allure


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