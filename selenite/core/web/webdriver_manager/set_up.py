from typing import Dict, Callable, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager

from selenite.core.web.selenium.typing import WebDriverOptions
from selenite.core.web.webdriver_manager import supported

installers: Dict[
    supported.BrowserName,
    Callable[[Optional[WebDriverOptions]], WebDriver]
] = {
    supported.chrome:
        lambda opts: webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=opts,
        ),
    supported.chromium:
        lambda opts: webdriver.Chrome(
            service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=opts,
        ),
    supported.firefox:
        lambda opts: webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=opts,
        ),
    supported.ie:
        lambda opts: webdriver.Ie(
            service=IEService(IEDriverManager().install()),
            options=opts,
        ),
    supported.edge:
        lambda ____: webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
        )
}


def local(
        name: supported.BrowserName = 'chrome',
        options: WebDriverOptions = None
) -> WebDriver:
    return installers[name](options)
