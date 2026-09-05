import allure
import pytest

from pages.login_page import LoginPage


@allure.suite("Test Login")
@allure.feature("Login Process")
class TestLogin:

    @pytest.fixture(autouse=True)
    def setup(self ,page):
        self.page = page
        self.login_page =LoginPage(self.page)

    @allure.step("Open Login Page")
    @allure.title("Login Page")
    @allure.description("Login Page")
    @pytest.mark.order(1)
    @pytest.mark.dependency(name="test_login_url")
    def test_login_url(self):
        with allure.step("Login Page"):
            self.login_page.open()

    @allure.step("Login ")
    @allure.title("Login ")
    @allure.description("Login ")
    @pytest.mark.order(2)
    ##@pytest.mark.dependency(depends = ["test_login_url"], name="test_login_with_valid_date")
    def test_login_with_valid_date(self):
        with allure.step("Login Page"):
            self.login_page.open()
            self.login_page.login()