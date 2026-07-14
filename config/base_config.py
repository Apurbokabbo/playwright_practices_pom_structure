from pathlib import Path
import os
from dotenv import load_dotenv


class BaseConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SCREEN_SHOT_DIR = BASE_DIR /"reports" /"screen_shot"
    LOGS_DIR = BASE_DIR /"logs"
    ENV_DIR = BASE_DIR /"config"/"environment"
    REPORTS_DIR = BASE_DIR /"reports"/"allure-reports"
    RECORD_VIDEOS_DIR = BASE_DIR /"reports"/"videos"


    load_dotenv(dotenv_path=BASE_DIR / ".env")

    ENV = os.getenv("ENV", "sit")
    HEADLESS = os.getenv("HEADLESS", "False").lower() in ("true", "yes", "1")
    BROWSER = os.getenv("BROWSER", "chromium").lower() 

