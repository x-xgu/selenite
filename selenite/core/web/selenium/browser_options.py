from urllib.parse import urljoin

from selenium import webdriver

from selenite import common
from selenite.conf.settings.project.selene import SeleneSettings

ARGS = [
    '--no-sandbox', '--disable-gpu', '--disable-notifications', '--disable-extensions', '--disable-dev-shm-usage',
    '--disable-setuid-sandbox', '--ignore-certificate-errors', '--hide-scrollbars',
]


def _chrome_options_with_automation():
    options = webdriver.ChromeOptions()
    [options.add_argument(_) for _ in ARGS]
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('credentials_enable_service', False)
    options.add_experimental_option('profile.password_manager_enabled', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return options


def _chrome_options_settings(setting: SeleneSettings):
    options = _chrome_options_with_automation()

    options.browser_version = setting.browser_version
    options.page_load_strategy = setting.browser_load_strategy
    options.add_argument(
        '--start-maximized'
        if setting.maximize_window
        else
        f'--window-size={setting.window_width},{setting.window_height}'
    )
    options.add_argument('--headless') if setting.headless else ...
    options.add_argument('--incognito') if setting.incognito else ...
    return options


def _selenoid_chrome_options(setting: SeleneSettings):
    setting.remote_videoName = f'video_{common.time.get_current_time()}.mp4'

    options = _chrome_options_settings(setting)

    options.set_capability('browserName', setting.browser_name)
    options.set_capability('browserVersion', setting.browser_version)
    options.set_capability(
        'selenoid:options', {
            'enableVNC': setting.remote_enableVNC,
            'enableVideo': setting.remote_enableVideo,
            'enableLog': setting.remote_enableLog,
            'sessionTimeout': setting.remote_sessionTimeout,
            'videoName': setting.remote_videoName,
        }
    )

    return options


def chrome_driver(setting: SeleneSettings):
    return lambda: (
        webdriver.Chrome(options=_chrome_options_settings(setting))
        if not setting.remote_url
        else webdriver.Remote(
            command_executor=urljoin(setting.remote_url, '/wd/hub'),
            options=_selenoid_chrome_options(setting)
        )
    )
