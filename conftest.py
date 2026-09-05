import os
import shutil
import pytest
import allure
from playwright.sync_api import sync_playwright
from config.base_config import BaseConfig
from utils.helpers import take_screenshot


# ==========================================
# Utility
# ==========================================

def clean_directory(directory):
    """Delete all files/folders inside a directory."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


# ==========================================
# Pytest Hooks
# ==========================================

def pytest_sessionstart(session):
    """Clean reports before execution."""
    clean_directory(BaseConfig.REPORT_DIR)
    print("[INFO] Cleaned report folders.")
    clean_directory(BaseConfig.SCREEN_SHOT_DIR)
    print("[INFO] Cleaned screenshots folders.")
    clean_directory(BaseConfig.RECORD_VIDEOS_DIR)
    print("[INFO] Cleaned video folders.")
    clean_directory(BaseConfig.LOGS_DIR)
    print("[INFO] Cleaned logs folders.")


def pytest_addoption(parser):
    parser.addoption(
        "--test-browser",
        action="store",
        default="chromium",
        help="chromium | firefox | webkit"
    )

    parser.addoption(
        "--headless",
        action="store",
        default="False",
        help="True | False"
    )


# ==========================================
# Playwright Fixtures
# ==========================================

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, pytestconfig):
    browser_name = pytestconfig.getoption("--test-browser").lower()
    headless = pytestconfig.getoption("--headless").lower() == "true"
    browser_type = getattr(playwright_instance, browser_name)
    browser = browser_type.launch(
        headless=headless,
        slow_mo=200
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def context(browser):
    BaseConfig.RECORD_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=str(BaseConfig.RECORD_VIDEOS_DIR),
        record_video_size={"width": 1920, "height": 1080}
    )
    yield context
    context.close()


@pytest.fixture(scope="session")
def page(context):
    page = context.new_page()
    yield page
    page.close()

# ==========================================
# Attach page to test class
# ==========================================

@pytest.fixture(scope="class", autouse=True)
def setup_page(request, page):
    """
    Makes self.page available in every test class.
    """
    if request.cls:
        request.cls.page = page
    yield

# ==========================================
# Screenshot after every test
# ==========================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    page = item.funcargs.get("page")
    if page is None:
        return
    try:
        screenshot = take_screenshot(page, item.name)
        allure.attach.file(
            str(screenshot),
            name=item.name,
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(e)


# ==========================================
# Attach Video Once After Suite
# ==========================================

def pytest_sessionfinish(session, exitstatus):
    page = getattr(session, "_page", None)
    if page:
        try:
            video_path = page.video.path()
            allure.attach.file(
                video_path,
                name="Execution Video",
                attachment_type=allure.attachment_type.MP4
            )
        except Exception:
            pass