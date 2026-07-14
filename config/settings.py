import yaml

from config.base_config import BaseConfig



ENV = BaseConfig.ENV
HEADLESS = BaseConfig.HEADLESS
BROWSER = BaseConfig.BROWSER


try:
    ymal_path = BaseConfig.ENV_DIR/f"{ENV}.ymal"
    with open(ymal_path, "r") as file:
        config_data = yaml.safe_load(file)
        BASE_URL = config_data["base_url"]
        print(BASE_URL)

except FileNotFoundError:

    print(f"No config file found at {BASE_URL}")
    BASE_URL = None