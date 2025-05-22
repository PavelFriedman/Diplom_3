import pytest
import requests
from selenium import webdriver
from data import Data
from urls import Urls


def pytest_addoption(parser):
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        help="Choose browser: chrome or firefox"
    )


@pytest.fixture
def driver(request):
    """Создание и закрытие драйвера/браузера без print."""
    browser = request.config.getoption("browser")
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise pytest.UsageError("--browser should be chrome or firefox")

    yield driver
    driver.quit()


@pytest.fixture()
def register_new_user_and_return_credentials():
    """
    Регистрация и удаление пользователя без установки токена в браузере.
    """
    payload = Data.USER_CREDENTIALS
    email = payload['email']
    password = payload['password']

    response = requests.post(Urls.create_user, json=payload)
    if response.status_code == 200:
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]
        yield email, password, access_token, refresh_token
        # удаляем пользователя по окончании теста
        headers = {"Authorization": access_token}
        requests.delete(Urls.user_data_management_url, headers=headers)
    else:
        pytest.fail(
            f"Не удалось зарегистрировать пользователя: "
            f"{response.status_code}, {response.text}"
        )


@pytest.fixture()
def login_user_via_localStorage(register_new_user_and_return_credentials, driver):
    """
    Установка токена сразу в браузере через localStorage.
    """
    email, password, access_token, refresh_token = register_new_user_and_return_credentials

    driver.get(Urls.BASE_URL)
    driver.execute_script(
        f"window.localStorage.setItem('accessToken', '{access_token}');"
    )
    driver.execute_script(
        f"window.localStorage.setItem('refreshToken', '{refresh_token}');"
    )
    driver.refresh()

    return email, password
