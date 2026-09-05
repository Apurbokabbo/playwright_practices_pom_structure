import os
import shutil
import sys
import pytest
from dotenv import load_dotenv

load_dotenv()

REPORT_DIR = "reports/allure-results"


def clean_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def main():
    clean_directory(REPORT_DIR)

    browser = os.getenv("BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "True")

    pytest_args = [
        "tests/ui/test_login.py",
        f"--test-browser={browser}",
        f"--headless={headless}",
        "--alluredir=reports/allure-results",
        "--clean-alluredir",
        "-v",
        "-s",
    ]

    exit_code = pytest.main(pytest_args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()