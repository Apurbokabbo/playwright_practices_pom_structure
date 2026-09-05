import json
from pathlib import Path
import allure

from config.settings import BASE_URL
from pages.base_page import BasePage
from utils.helpers import take_screenshot


class LoginPage(BasePage):
    TEST_DATA_FILE = Path(__file__).resolve().parent.parent /"data"/ "login.json"


    @staticmethod
    def setup_test_data(self):
        try:
            file_path = Path(__file__).resolve().parent.parent /"data"/ "login.json"
            with open(file_path, "r") as file:
                data = json.load(file)
                if not data or not isinstance(data,dict) or len(data) == 0:
                    raise FileNotFoundError(f"Login file not found at {file_path}")
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Login file not found at {file_path}")
        except json.decoder.JSONDecodeError:
            raise FileNotFoundError(f"Login file not found at {file_path}")
        except RuntimeError:
            raise FileNotFoundError(f"Login file not found at {file_path}")



    TEST_DATA = setup_test_data()


    def __init__(self,page):
        super().__init__(page)
        self.test_data = self.TEST_DATA

    def load_json_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if not data:
                    raise ValueError(f"Login file not found at {file_path}")
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Login file not found at {file_path}")
        except json.decoder.JSONDecodeError:
            raise FileNotFoundError(f"Login file not found at {file_path}")
        except RuntimeError:
            raise FileNotFoundError(f"Login file not found at {file_path}")



    def open (self):
        self.logger.info("open url")
        self.page.goto(BASE_URL,wait_until = "domcontentloaded")
        screenshot_path = take_screenshot(self.page,"open_url")
        allure.attach.file((screenshot_path) ,name ="open url", attachment_type=allure.attachment_type.PNG)

