import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = None  # Должен быть задан в дочерних классах

    @allure.step("Открытие страницы")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Ввод текста в поле")
    def fill_input(self, locator, text):
        """Подождать появления инпута и ввести значение"""
        self.wait_visibility_of_element(locator)
        self.driver.find_element(*locator).send_keys(text)

    @allure.step("Ожидание видимости элемента")
    def wait_visibility_of_element(self, locator):
        """Ждёт, пока элемент станет видимым"""
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание невидимости элемента")
    def wait_invisibility_of_element(self, locator, timeout=10):
        """Ждёт, пока элемент станет невидимым"""
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.invisibility_of_element_located(locator)
        )

    @allure.step("Клик по элементу")
    def click_on_element(self, locator):
        """Кликает по элементу после ожидания кликабельности"""
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable(locator)
        )
        self.driver.find_element(*locator).click()

    @allure.step("Получение текста элемента")
    def get_text_element(self, locator):
        """Возвращает текст указанного элемента"""
        return self.driver.find_element(*locator).text

    @allure.step("Получение текстов всех элементов")
    def get_texts_from_elements(self, locator):
        """Возвращает список текстов всех элементов по локатору"""
        self.wait_visibility_of_element(locator)
        elements = self.driver.find_elements(*locator)
        return [item.text.strip() for item in elements]

    @allure.step("Получение текущего URL")
    def get_current_url(self, expected_url=None, timeout=10):
        """Получает текущий URL. Если передан expected_url, ждёт его появления."""
        if expected_url:
            WebDriverWait(self.driver, timeout).until(
                expected_conditions.url_to_be(expected_url)
            )
        return self.driver.current_url

    @allure.step("Проверка исчезновения элемента")
    def is_disappeared(self, locator, timeout=10):
        """Ждёт исчезновения элемента из DOM"""
        WebDriverWait(self.driver, timeout, 1).until_not(
            expected_conditions.presence_of_element_located(locator)
        )

    @allure.step("Проверка видимости элемента")
    def is_element_visible(self, locator):
        """Проверяет видимость элемента на странице"""
        try:
            self.wait_visibility_of_element(locator)
            return True
        except TimeoutException:
            return False

    @allure.step("Проверка закрытия модального окна")
    def is_modal_closed(self, locator, timeout=10):
        """Проверяет, что модальное окно закрылось"""
        try:
            self.is_disappeared(locator)
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание открытия модального окна")
    def wait_modal_opened(self, locator):
        """Ждёт появления модального окна"""
        self.wait_visibility_of_element(locator)

    @allure.step("Ожидание закрытия модального окна")
    def wait_modal_closed(self, locator):
        """Ждёт исчезновения модального окна"""
        self.is_disappeared(locator)

    @allure.step("Прокрутка к элементу и клик")
    def scroll_to_and_click(self, locator):
        """Скроллит до элемента и кликает по нему"""
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(locator)
        )
        element.click()