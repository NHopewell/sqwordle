from dataclasses import dataclass

import sqwordle.settings as settings
import selenium.webdriver as Webdriver


@dataclass
class Driver:
    """Selenium automation requires a webdriver, in our case a chromewebdriver,
    this class sets the chromedriver options and provides a driver with these
    options.
    """

    timeout_long: int = 5
    timeout_short: int = 2
    path = settings.DRIVER_LOCATION

    options = Webdriver.ChromeOptions()

    # options.add_argument(" - incognito")
    options.add_argument("start-maximized")
    # options.add_argument("--disable-web-security")
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument(
    #    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    # )

    @classmethod
    def get_driver(cls) -> Webdriver:
        """Return a chromedriver with all opitions bound."""
        driver = Webdriver.Chrome(
            executable_path=cls.path, options=cls.options
        )
        return driver
