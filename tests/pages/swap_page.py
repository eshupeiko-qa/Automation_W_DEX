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