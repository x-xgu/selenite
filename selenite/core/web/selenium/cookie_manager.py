from typing import Dict

from selene import Browser


def current_browser_cookie(browser: Browser) -> str:
    cookies_dict: Dict[str, str] = {}

    for cookie in browser.config.driver.get_cookies():
        cookies_dict[cookie['name']] = cookie['value']
    return '; '.join([f"{name}={value}" for name, value in cookies_dict.items()])
