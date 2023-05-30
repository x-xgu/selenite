from __future__ import annotations

from pathlib import Path
from typing import Optional, Union, Literal

from pydantic import BaseSettings

BrowserType = Literal['chrome', 'chromium', 'firefox', 'ie', 'edge']

Scope = Literal['session', 'package', 'module', 'class', 'method', 'function']


class SeleneSettings(BaseSettings):
    """
    Selene settings
    """
    browser_name: BrowserType = ''
    browser_version: str = ''
    browser_load_strategy: str = ''

    browser_management_scope: Scope = ''

    base_url: str = ''

    timeout: float = 5.0

    maximize_window: bool = False
    window_width: int = 1920
    window_height: int = 1080

    headless: bool = False
    incognito: bool = False

    remote_url: Optional[str] = ''
    remote_sessionTimeout: str = ''
    remote_enableVNC: bool = False
    remote_enableVideo: bool = False
    remote_enableLog: bool = False
    remote_videoName: str = ''

    hold_browser_open: bool = False
    save_screenshot_on_failure: bool = False
    save_page_source_on_failure: bool = False
    save_case_video_on_failure: bool = False

    @classmethod
    def in_context(
            cls,
            env: Union[str, Path]
    ) -> SeleneSettings:
        """
        Get settings in context
        """
        return cls(
            _env_file=env
        )
