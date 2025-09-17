from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SwapPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # === Локаторы ===
    FROM_TOKEN_SYMBOL = (By.XPATH, '//input[@id="amount-POL"]//ancestor::div//span[text()="POL"]')
    TO_TOKEN_SYMBOL = (By.XPATH, '//input[@id="amount-USDT0"]//ancestor::div//span[text()="USDT"]')

    AMOUNT_INPUT_POL = (By.ID, "amount-POL")
    AMOUNT_INPUT_USDT = (By.ID, "amount-USDT0")

    MAX_BUTTON_POL = (By.XPATH, '//input[@id="amount-POL"]//following::button[text()="Max"]')
    MAX_BUTTON_USDT = (By.XPATH, '//input[@id="amount-USDT0"]//following::button[text()="Max"]')

    INVERT_BUTTON = (By.XPATH, '//button[.//*[local-name()="svg"]]')  # Кнопка с SVG-стрелкой

    SWAP_BUTTON_DISABLED = (By.XPATH, '//button[@disabled and contains(., "Enter an amount")]')
    SWAP_BUTTON_ENABLED = (By.XPATH, '//button[not(@disabled) and .//span[text()="Swap"]]')

    BALANCE_POL = (By.XPATH, '//input[@id="amount-POL"]//preceding::span[text()="Balance: "]//following-sibling::span')
    BALANCE_USDT = (By.XPATH, '//input[@id="amount-USDT0"]//preceding::span[text()="Balance: "]//following-sibling::span')

    SWAP_TAB_ACTIVE = (By.XPATH, '//a[@href="/swap" and @aria-current="page"]')
    POOLS_LINK = (By.XPATH, '//a[@href="/pools" and contains(text(), "Pools")]')
    
    # Web3 элементы (из предоставленного HTML)
    DEX_LOGO = (By.CSS_SELECTOR, "header img[src*='dex-logo']")
    HEADER = (By.CSS_SELECTOR, "header.sticky")
    NETWORK_BUTTON = (By.CSS_SELECTOR, "wui-network-button")
    ACCOUNT_BUTTON = (By.CSS_SELECTOR, "wui-account-button")
    ACCOUNT_ADDRESS = (By.CSS_SELECTOR, "wui-avatar[address]")
    W3M_MODAL = (By.CSS_SELECTOR, "w3m-modal")
    MOBILE_MENU_BUTTON = (By.CSS_SELECTOR, ".min-[960px]\\:hidden button")
    DESKTOP_WALLET_AREA = (By.CSS_SELECTOR, ".hidden.min-[960px]\\:block")

    # === Методы ===

    def wait_for_page_load(self):
        """Ждём, пока страница загрузится"""
        self.wait.until(EC.presence_of_element_located(self.SWAP_TAB_ACTIVE))

    def get_from_token(self):
        """Возвращает символ токена в поле 'From'"""
        elem = self.wait.until(EC.presence_of_element_located(self.FROM_TOKEN_SYMBOL))
        return elem.text

    def get_to_token(self):
        """Возвращает символ токена в поле 'To'"""
        elem = self.wait.until(EC.presence_of_element_located(self.TO_TOKEN_SYMBOL))
        return elem.text

    def enter_amount_pol(self, amount):
        """Вводит сумму в поле POL"""
        input_field = self.wait.until(EC.element_to_be_clickable(self.AMOUNT_INPUT_POL))
        input_field.clear()
        input_field.send_keys(str(amount))

    def click_max_pol(self):
        """Нажимает Max для POL"""
        button = self.wait.until(EC.element_to_be_clickable(self.MAX_BUTTON_POL))
        button.click()

    def click_invert(self):
        """Нажимает кнопку инверсии"""
        button = self.wait.until(EC.element_to_be_clickable(self.INVERT_BUTTON))
        button.click()

    def is_swap_button_enabled(self):
        """Проверяет, активна ли кнопка Swap"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.SWAP_BUTTON_ENABLED))
            return True
        except:
            return False

    def get_balance_pol(self):
        """Получает баланс POL"""
        elem = self.wait.until(EC.visibility_of_element_located(self.BALANCE_POL))
        return float(elem.text)

    def get_balance_usdt(self):
        """Получает баланс USDT"""
        elem = self.wait.until(EC.visibility_of_element_located(self.BALANCE_USDT))
        return float(elem.text)

    def get_input_value_pol(self):
        """Получает значение из поля POL"""
        input_field = self.driver.find_element(*self.AMOUNT_INPUT_POL)
        return input_field.get_attribute("value")

    def get_input_value_usdt(self):
        """Получает значение из поля USDT"""
        input_field = self.driver.find_element(*self.AMOUNT_INPUT_USDT)
        return input_field.get_attribute("value")

    def navigate_to_pools(self):
        """Переходит на вкладку Pools"""
        link = self.wait.until(EC.element_to_be_clickable(self.POOLS_LINK))
        link.click()
    
    # === Дополнительные Web3 методы ===
    
    def is_logo_visible(self):
        """Проверяет, виден ли логотип DEX"""
        try:
            logo = self.wait.until(EC.presence_of_element_located(self.DEX_LOGO))
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
        """Возвращает баланс аккаунта из Web3 кнопки"""
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
    
    def is_w3m_modal_present(self):
        """Проверяет, присутствует ли Web3 модал на странице"""
        try:
            self.driver.find_element(*self.W3M_MODAL)
            return True
        except:
            return False
    
    def click_logo(self):
        """Нажимает на логотип DEX"""
        logo_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "header a[href='/']")))
        logo_link.click()
    
    def is_mobile_menu_visible(self):
        """Проверяет, видно ли мобильное меню"""
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