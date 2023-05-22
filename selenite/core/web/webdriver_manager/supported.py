from typing import Literal, Final

BrowserName = Literal['chrome', 'chromium', 'firefox', 'ie', 'edge']

chrome: Final[BrowserName] = 'chrome'
chromium: Final[BrowserName] = 'chromium'
firefox: Final[BrowserName] = 'firefox'
ie: Final[BrowserName] = 'ie'
edge: Final[BrowserName] = 'edge'
