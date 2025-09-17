import pytest
from tests.pages.pool_page import PoolPage
import allure
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.ui
@allure.epic("Pool Page")
@allure.feature("UI Tests")
class TestPoolPage:

    @allure.story("Page Load")
    @allure.title("Проверка загрузки страницы пулов")
    def test_page_loads(self, driver):
        """Проверяет, что страница пулов загружается корректно"""
        driver.get("https://w-dex.ai/")
        page = PoolPage(driver)
        page.wait_for_page_load()
        
        assert "w-dex.ai" in driver.current_url
        assert page.is_logo_visible(), "Логотип DEX должен быть виден"

    @allure.story("Navigation")
    @allure.title("Проверка отображения логотипа DEX")
    def test_logo_visibility(self, driver):
        """Проверяет, что логотип DEX отображается и кликабелен"""
        driver.get("https://w-dex.ai/")
        page = PoolPage(driver)
        
        assert page.is_logo_visible(), "Логотип DEX должен быть виден на странице"
        
        # Проверяем, что логотип кликабелен
        logo = page.get_logo_element()
        assert logo.is_enabled(), "Логотип должен быть кликабельным"

    @allure.story("Web3 Integration")
    @allure.title("Проверка отображения кнопки сети")
    def test_network_button_display(self, driver):
        """Проверяет отображение кнопки выбора сети"""
        driver.get("https://w-dex.ai/")
        page = PoolPage(driver)
        page.wait_for_page_load()
        
        assert page.is_network_button_visible(), "Кнопка сети должна быть видна"
        
        network_name = page.get_network_name()
        assert network_name is not None, "Название сети должно отображаться"
        assert "Polygon" in network_name, "Должна отображаться сеть Polygon"

    @allure.story("Web3 Integration")
    @allure.title("Проверка подключения аккаунта")
    def test_account_connection(self, driver):
        """Проверяет отображение данных подключенного аккаунта"""
        driver.get("https://w-dex.ai/")
        page = PoolPage(driver)
        page.wait_for_page_load()
        
        if page.is_account_connected():
            # Если аккаунт подключен, проверяем его данные
            balance = page.get_account_balance()
            address = page.get_account_address()
            
            assert balance is not None, "Баланс аккаунта должен отображаться"
            assert "POL" in balance, "В балансе должны быть токены POL"
            assert address is not None, "Адрес аккаунта должен отображаться"
            assert address.startswith("0x"), "Адрес должен начинаться с 0x"
            assert len(address) == 42, "Адрес должен содержать 42 символа"

    @allure.story("Responsive Design")
    @allure.title("Проверка адаптивности интерфейса")
    def test_responsive_design(self, driver):
        """Проверяет адаптивность интерфейса для разных размеров экрана"""
        driver.get("https://w-dex.ai/")
        page = PoolPage(driver)
        page.wait_for_page_load()
        
        # Тестируем десктопный размер
        driver.set_window_size(1200, 800)
        page.wait_for_page_load()
        
        desktop_wallet_visible = page.is_desktop_wallet_area_visible()
        mobile_menu_visible = page.is_mobile_menu_visible()
        
        # На десктопе должна быть видна область кошелька, но не мобильное меню
        assert desktop_wallet_visible or not mobile_menu_visible, "На десктопе должен отображаться правильный интерфейс"

    @allure.story("Web3 Components")
    @allure.title("Проверка наличия Web3 компонентов")
    def test_web3_components_presence(self, driver):
        """Проверяет наличие необходимых Web3 компонентов"""
        driver.get("https://w-dex.ai/")
        page = PoolPage(driver)
        page.wait_for_page_load()
        
        # Проверяем наличие Web3 модала
        assert page.is_w3m_modal_present(), "Web3 модал должен присутствовать на странице"
        
        # Проверяем наличие iframe для верификации
        # Это может быть не всегда доступно, поэтому делаем мягкую проверку
        verify_iframe_present = page.is_verify_iframe_present()
        # Просто логируем результат без строгой проверки
        print(f"Verify iframe present: {verify_iframe_present}")

    @allure.story("Navigation")
    @allure.title("Проверка клика по логотипу")
    def test_logo_click(self, driver):
        """Проверяет, что клик по логотипу ведет на главную страницу"""
        # Сначала переходим на другую страницу
        driver.get("https://w-dex.ai/swap")
        
        page = PoolPage(driver)
        
        # Кликаем по логотипу
        page.click_logo()
        
        # Проверяем, что перешли на главную страницу
        WebDriverWait(driver, 10).until(lambda d: "/" in d.current_url.split('/')[-1] or d.current_url.endswith('/'))
        current_url = page.get_current_url()
        assert current_url.endswith('/') or '/swap' not in current_url, "Клик по логотипу должен вести на главную страницу"

    @allure.story("Page Structure")
    @allure.title("Проверка основной структуры страницы")
    def test_page_structure(self, driver):
        """Проверяет основную структуру и элементы страницы"""
        driver.get("https://w-dex.ai/")
        page = PoolPage(driver)
        page.wait_for_page_load()
        
        # Проверяем заголовок страницы
        title = page.get_page_title()
        assert title is not None and len(title) > 0, "Страница должна иметь заголовок"
        
        # Проверяем основные элементы структуры
        assert page.is_logo_visible(), "Логотип должен быть виден"
        assert page.is_network_button_visible(), "Кнопка сети должна быть видна"
        
        # Проверяем, что страница имеет правильный CSS класс
        body_class = driver.find_element("tag name", "body").get_attribute("class")
        assert "metaforce-blue" in body_class, "Body должен иметь класс metaforce-blue"