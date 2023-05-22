from __future__ import annotations

from typing import Callable

from selene import be, Collection, have, query, Element
from selene.support.shared.jquery_style import ss
from selenium.webdriver.support.select import Select


class LocatorConfig:
    locate_function: Callable = None

    def behind_label(self, label_value: str) -> Element:
        return self.s_behind_label(label_value).element_by(be.enabled)

    def s_behind_label(self, label_value: str) -> Collection:
        return ss(self.locate_function(label_value, self.tag))

    def __getattr__(self, tag: str) -> LocatorConfig:
        self.tag = tag
        return self


class EditPage(LocatorConfig):
    select_option: Collection = None

    def input_text_after_label(self, label: str, text: str) -> EditPage:
        self.input.behind_label(label).click().clear().type(text)
        return self

    def input_long_text_after_label(self, label: str, long_text: str) -> EditPage:
        self.textarea.behind_label(label).click().clear().type(long_text)
        return self

    def click_checkbox_after_label(self, label: str) -> EditPage:
        self.input.behind_label(label).click()
        return self

    def input_text_after_label_and_select_self(self, label: str, text: str) -> EditPage:
        self.input_text_after_label(label, text)
        self.select_option.by(have.text(text)).element_by(be.clickable).click()
        return self

    def input_text_after_label_and_select_option(self, label: str, text: str, option: str) -> EditPage:
        self.input_text_after_label(label, text)
        self.select_option.by(have.text(option)).element_by(be.clickable).click()
        return self

    def click_input_box_after_label_and_select_option(self, label: str, option: str) -> EditPage:
        self.input.behind_label(label).click()
        self.select_option.by(have.text(option)).element_by(be.clickable).click()
        return self

    def click_button_after_label(self, label: str) -> EditPage:
        self.button.behind_label(label).click()
        return self

    def select_dropdown_menu_after_label(self, label: str, option: str) -> EditPage:
        Select(self.select.behind_label(label).locate()).select_by_visible_text(option)
        return self

    def get_text_after_label(self, label: str) -> str:
        text = self.span.behind_label(label).get(query.text)
        return text
