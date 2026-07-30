import logging
from config.base_config import BaseConfig
from pathlib import Path
from datetime import datetime

def take_screenshot(page, name):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = Path(BaseConfig.SCREEN_SHOT_DIR)
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"{name}_{timestamp}.png"
        page.wait_for_load_state("networkidle", timeout=10000)
        page.screenshot(
            path=str(file_path),
            timeout=60000,
            full_page=True
        )
        return file_path   # <-- IMPORTANT
    except Exception as e:
        logging.exception(f"Failed to take screenshot: {e}")
        return None

def highlight_element(page, selector, color="yellow", duration=0.5):
    page.eval_on_selector(
        selector,
        f"""(el) => {{
            const original = el.style.border;
            el.style.color = "2px solid {color}";
            setTimeout(()=> el.style.border = original, {int(duration * 1000)});
        }}"""
    )