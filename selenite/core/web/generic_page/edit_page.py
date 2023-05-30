from __future__ import annotations

from typing import Callable

from loguru import logger
from selene import be, Collection, have, query, Element
from selene.support.shared.jquery_style import ss
from selenium.webdriver.support.select import Select


class LocatorConfig:
    """
    LocatorConfig is a class that provides a convenient way to locate elements.
    """
    locate_function: Callable = None

    def behind_label(self, label_value: str) -> Element:
        """
        Locate element behind label
        """
        return self.s_behind_label(label_value).element_by(be.enabled)

    def s_behind_label(self, label_value: str) -> Collection:
        """
        Locate elements behind label
        """
        return ss(self.locate_function(label_value, self.tag))

    def __getattr__(self, tag: str) -> LocatorConfig:
        """
        Set tag
        """
        self.tag = tag
        return self


LOG_TAG = 'EDIT_PAGE'


class EditPage(LocatorConfig):
    """
    EditPage is a class that provides a convenient way to edit elements.
    """
    select_option: Collection = None

    def input_text_after_label(self, label: str, text: str) -> EditPage:
        """
        Input text after label
        """
        logger.debug(f"[{LOG_TAG}] Input text after label: {label} with text: {text}")
        self.input.behind_label(label).click().clear().type(text)
        return self

    def input_long_text_after_label(self, label: str, long_text: str) -> EditPage:
        """
        Input long text after label
        """
        logger.debug(f"[{LOG_TAG}] Input long text after label: {label} with text: {long_text}")
        self.textarea.behind_label(label).click().clear().type(long_text)
        return self

    def click_checkbox_after_label(self, label: str) -> EditPage:
        """
        Click checkbox after label
        """
        logger.debug(f"[{LOG_TAG}] Click checkbox after label: {label}")
        self.input.behind_label(label).click()
        return self

    def input_text_after_label_and_select_self(self, label: str, text: str) -> EditPage:
        """
        Input text after label and select self
        """
        logger.debug(f"[{LOG_TAG}] Input text after label: {label} with text: {text} and select self")
        self.input_text_after_label(label, text)
        self.select_option.by(have.text(text)).element_by(be.clickable).click()
        return self

    def input_text_after_label_and_select_option(self, label: str, text: str, option: str) -> EditPage:
        """
        Input text after label and select option
        """
        logger.debug(f"[{LOG_TAG}] Input text after label: {label} with text: {text} and select option: {option}")
        self.input_text_after_label(label, text)
        self.select_option.by(have.text(option)).element_by(be.clickable).click()
        return self

    def click_input_box_after_label_and_select_option(self, label: str, option: str) -> EditPage:
        """
        Click input box after label and select option
        """
        logger.debug(f"[{LOG_TAG}] Click input box after label: {label} and select option: {option}")
        self.input.behind_label(label).click()
        self.select_option.by(have.text(option)).element_by(be.clickable).click()
        return self

    def click_button_after_label(self, label: str) -> EditPage:
        """
        Click button after label
        """
        logger.debug(f"[{LOG_TAG}] Click button after label: {label}")
        self.button.behind_label(label).click()
        return self

    def select_dropdown_menu_after_label(self, label: str, option: str) -> EditPage:
        """
        Select dropdown menu after label
        """
        logger.debug(f"[{LOG_TAG}] Select dropdown menu after label: {label} with option: {option}")
        Select(self.select.behind_label(label).locate()).select_by_visible_text(option)
        return self

    def get_text_after_label(self, label: str) -> str:
        """
        Get text after label
        """
        logger.debug(f"[{LOG_TAG}] Get text after label: {label}")
        text = self.span.behind_label(label).get(query.text)
        return text
