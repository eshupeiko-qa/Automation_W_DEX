from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # === Локаторы ===
    
    # Хедер и навигация
    DEX_LOGO = (By.CSS_SELECTOR, "header img[src*='dex-logo']")
    HEADER = (By.CSS_SELECTOR, "header.sticky")
    NAVIGATION = (By.CSS_SELECTOR, "nav.flex.justify-center")
    
    # Web3 элементы
    NETWORK_BUTTON = (By.CSS_SELECTOR, "wui-network-button")
    NETWORK_BUTTON_TEXT = (By.CSS_SELECTOR, "wui-network-button wui-text")
    ACCOUNT_BUTTON = (By.CSS_SELECTOR, "wui-account-button")
    ACCOUNT_BALANCE = (By.CSS_SELECTOR, "wui-account-button wui-text")
    ACCOUNT_ADDRESS = (By.CSS_SELECTOR, "wui-avatar[address]")
    
    # Мобильное меню
    MOBILE_MENU_BUTTON = (By.CSS_SELECTOR, ".min-[960px]\\:hidden button")
    DESKTOP_WALLET_AREA = (By.CSS_SELECTOR, ".hidden.min-[960px]\\:block")
    
    # Web3 модал
    W3M_MODAL = (By.CSS_SELECTOR, "w3m-modal")
    W3M_BUTTON = (By.CSS_SELECTOR, "w3m-button")
    
    # Верификационный iframe
    VERIFY_IFRAME = (By.ID, "verify-api")

    # === Методы ===

    def wait_for_page_load(self):
        """Ждём, пока страница загрузится"""
        self.wait.until(EC.presence_of_element_located(self.HEADER))
        self.wait.until(EC.presence_of_element_located(self.DEX_LOGO))

    def get_logo_element(self):
        """Возвращает элемент логотипа DEX"""
        return self.wait.until(EC.presence_of_element_located(self.DEX_LOGO))

    def is_logo_visible(self):
        """Проверяет, виден ли логотип DEX"""
        try:
            logo = self.get_logo_element()
            return logo.is_displayed()
        except:
            return False

    def get_network_name(self):
        """Возвращает название текущей сети"""
        try:
            network_button = self.wait.until(EC.presence_of_element_located(self.NETWORK_BUTTON))
            return network_button.text.strip()
        except:
            return None

    def is_network_button_visible(self):
        """Проверяет, видна ли кнопка сети"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.NETWORK_BUTTON))
            return True
        except:
            return False

    def get_account_balance(self):
        """Возвращает баланс аккаунта"""
        try:
            account_button = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_BUTTON))
            balance_text = account_button.get_attribute("balance")
            return balance_text
        except:
            return None

    def get_account_address(self):
        """Возвращает адрес аккаунта"""
        try:
            avatar = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_ADDRESS))
            return avatar.get_attribute("address")
        except:
            return None

    def is_account_connected(self):
        """Проверяет, подключен ли аккаунт"""
        try:
            self.wait.until(EC.presence_of_element_located(self.ACCOUNT_BUTTON))
            return True
        except:
            return False

    def click_mobile_menu(self):
        """Нажимает на мобильное меню"""
        mobile_button = self.wait.until(EC.element_to_be_clickable(self.MOBILE_MENU_BUTTON))
        mobile_button.click()

    def is_mobile_menu_visible(self):
        """Проверяет, видно ли мобильное меню (для экранов меньше 960px)"""
        try:
            mobile_area = self.driver.find_element(*self.MOBILE_MENU_BUTTON)
            return mobile_area.is_displayed()
        except:
            return False

    def is_desktop_wallet_area_visible(self):
        """Проверяет, видна ли область кошелька на десктопе"""
        try:
            desktop_area = self.driver.find_element(*self.DESKTOP_WALLET_AREA)
            return desktop_area.is_displayed()
        except:
            return False

    def is_w3m_modal_present(self):
        """Проверяет, присутствует ли Web3 модал на странице"""
        try:
            self.driver.find_element(*self.W3M_MODAL)
            return True
        except:
            return False

    def is_verify_iframe_present(self):
        """Проверяет, присутствует ли iframe для верификации"""
        try:
            iframe = self.driver.find_element(*self.VERIFY_IFRAME)
            return iframe.is_present()
        except:
            return False

    def get_page_title(self):
        """Возвращает заголовок страницы"""
        return self.driver.title

    def click_logo(self):
        """Нажимает на логотип DEX"""
        logo_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "header a[href='/']")))
        logo_link.click()

    def wait_for_network_switch(self, expected_network):
        """Ждёт переключения на указанную сеть"""
        self.wait.until(lambda driver: self.get_network_name() == expected_network)

    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url