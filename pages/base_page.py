from utils.logger import setup_logger
from utils.helpers import highlight_element
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:
    def __init__(self, page):
        self.page = page
        self.logger = setup_logger(self.__class__.__name__)
        self.default_timeout = 60000  # milliseconds

    def perform_with_retry(self, action, description,
                           retries=3,
                           delay=1):

        for attempt in range(1, retries + 1):
            try:
                return action()

            except PlaywrightTimeoutError as e:

                self.logger.warning(
                    f"{description} failed "
                    f"(Attempt {attempt}/{retries})"
                )

                if attempt == retries:
                    raise

                self.page.wait_for_timeout(delay * 1000)

    # ---------- Core Waits ----------
    def wait_for_visible(self, selector, timeout=None):
        try:
            self.logger.info(f"Waiting for {selector} to be visible.")
            self.page.locator(selector).wait_for(state="visible", timeout=timeout or self.default_timeout)
        except PlaywrightTimeoutError:
            self.logger.error(f"Element {selector} not visible after timeout.")
            raise

    def wait_for_attached(self, selector, timeout=None):
        self.logger.info(f"Waiting for {selector} to be attached to DOM.")
        self.page.locator(selector).wait_for(state="attached", timeout=timeout or self.default_timeout)

    def wait_for_enabled(self, selector, timeout=None):
        self.logger.info(f"Waiting for {selector} to be enabled.")
        self.page.locator(selector).wait_for(state="enabled", timeout=timeout or self.default_timeout)

    def wait_for_hidden(self, selector, timeout=None):
        self.logger.info(f"Waiting for {selector} to disappear.")
        self.page.locator(selector).wait_for(state="hidden", timeout=timeout or self.default_timeout)

    # ---------- Element Actions ----------
    # ---------- Element Actions ----------
    def click(self, selector):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Clicking {selector}")
            self.page.click(selector)

        self.perform_with_retry(action, f"Click {selector}")

    def double_click(self, selector):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Double-clicking {selector}")
            self.page.dblclick(selector)

        self.perform_with_retry(action, f"Double Click {selector}")

    def enter_text(self, selector, text, clear_first=True):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Entering text '{text}' in {selector}")

            if clear_first:
                self.page.fill(selector, "")

            self.page.fill(selector, text)

        self.perform_with_retry(action, f"Enter text into {selector}")

    def append_text(self, selector, text):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Appending text '{text}' in {selector}")
            self.page.type(selector, text)

        self.perform_with_retry(action, f"Append text into {selector}")

    def select_dropdown(self, selector, option_text):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Selecting option '{option_text}' in {selector}")
            self.page.select_option(selector, label=option_text)

        self.perform_with_retry(action, f"Select dropdown {selector}")

    def get_text(self, selector):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            text = self.page.locator(selector).inner_text()
            self.logger.info(f"Text from {selector}: '{text}'")
            return text

        return self.perform_with_retry(action, f"Get text from {selector}")

    def get_attribute(self, selector, attribute_name):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            attr = self.page.locator(selector).get_attribute(attribute_name)
            self.logger.info(f"Attribute '{attribute_name}' of {selector}: '{attr}'")
            return attr

        return self.perform_with_retry(
            action,
            f"Get attribute '{attribute_name}' from {selector}"
        )

    def is_visible(self, selector):
        def action():
            visible = self.page.locator(selector).is_visible()
            self.logger.info(f"Visibility of {selector}: {visible}")
            return visible

        return self.perform_with_retry(action, f"Check visibility of {selector}")

    def is_enabled(self, selector):
        def action():
            enabled = self.page.locator(selector).is_enabled()
            self.logger.info(f"Enabled state of {selector}: {enabled}")
            return enabled

        return self.perform_with_retry(action, f"Check enabled state of {selector}")

    def is_checked(self, selector):
        def action():
            checked = self.page.locator(selector).is_checked()
            self.logger.info(f"Checked state of {selector}: {checked}")
            return checked

        return self.perform_with_retry(action, f"Check checked state of {selector}")

    # ---------- User-Like Actions ----------
    def hover(self, selector):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Hovering over {selector}")
            self.page.hover(selector)

        self.perform_with_retry(action, f"Hover over {selector}")

    def scroll_into_view(self, selector):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Scrolling into view {selector}")
            self.page.locator(selector).scroll_into_view_if_needed()

        self.perform_with_retry(action, f"Scroll into view {selector}")

    def take_element_screenshot(self, selector, path):
        def action():
            self.wait_for_visible(selector)
            highlight_element(self.page, selector)
            self.logger.info(f"Taking screenshot of {selector}")
            self.page.locator(selector).screenshot(path=path)

        self.perform_with_retry(action, f"Screenshot {selector}")

    # ---------- Assertions ----------
    def assert_text(self, selector, expected_text):
        def action():
            actual_text = self.get_text(selector)
            assert actual_text == expected_text, (
                f"Expected: '{expected_text}', Got: '{actual_text}'"
            )

        self.perform_with_retry(action, f"Assert text of {selector}")

    def assert_element_visible(self, selector):
        def action():
            highlight_element(self.page, selector)
            assert self.is_visible(selector), (
                f"Element {selector} should be visible"
            )

        self.perform_with_retry(action, f"Assert visibility of {selector}")

    def assert_element_not_visible(self, selector):
        def action():
            highlight_element(self.page, selector)
            assert not self.is_visible(selector), (
                f"Element {selector} should not be visible"
            )

        self.perform_with_retry(action, f"Assert invisibility of {selector}")

    # ---------- Utility ----------
    def reload_page(self):
        def action():
            self.logger.info("Reloading the page.")
            self.page.reload(wait_until="load")

        self.perform_with_retry(action, "Reload page")

    def go_to(self, url):
        def action():
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until="load")

        self.perform_with_retry(action, f"Navigate to {url}")

    def execute_script(self, script: str):
        def action():
            self.logger.info(f"Executing JavaScript: {script}")
            return self.page.evaluate(script)

        return self.perform_with_retry(action, "Execute JavaScript")

    def get_current_url(self):
        def action():
            url = self.page.url
            self.logger.info(f"Retrieved current URL: '{url}'")
            return url

        return self.perform_with_retry(action, "Get current URL")