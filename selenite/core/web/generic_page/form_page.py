from __future__ import annotations

import time
from typing import List, Union, Callable, Dict

from selene import Collection, by, query, have, be, Element

from selenite import common
from selenite.common.web_assert import web_assert


class Entity:
    thead: Collection = None
    tbody: Collection = None
    child: str = '*'

    @property
    def ths(self) -> List[str]:
        return [_.get(query.text) for _ in self.thead]

    @property
    def table_element_list(self) -> List[List[Element]]:
        return [[_ for _ in row.all(by.xpath(self.child))] for row in self.tbody]

    @property
    def table_text_list(self) -> List[List[str]]:
        i = self.table_element_list
        text_list = [[_.get(query.text) for _ in __] for __ in i]
        return text_list

    @property
    def table_row_size(self) -> int:
        return len(self.tbody)

    def matching_elements_in_table_by_row_keyword(self, row_keyword: Union[str, list]) -> Collection:
        elements = self.tbody
        for keyword in ([row_keyword] if isinstance(row_keyword, str) else row_keyword):
            elements = elements.by(have.text(keyword))
            if len(elements) == 0:
                break
        return elements


class FormPage(Entity):

    def get_row_attribute_by_index(self, index: int, attribute: str) -> str:
        i = self.ths.index(attribute)
        text = self.tbody.element(index).all(by.xpath(self.child)).element(i).get(query.text)
        return text

    def get_row_attribute_by_text(self, row_keyword: Union[str, list], attribute) -> str:
        i = self.ths.index(attribute)
        elements = self.matching_elements_in_table_by_row_keyword(row_keyword)
        text = (
            elements.element_by(be.visible).all(by.xpath(self.child)).element(i).get(query.text)
        ) if len(elements) else None
        return text

    def contains_sub_dictionary(self, dictionary: dict) -> bool:
        return bool(
            common.matching.matching_dictionaries(
                common.convert.zip_dict(
                    self.ths,
                    *self.table_text_list)
            ).by_exact_dictionary(dictionary)
        )

    def should_contain_sub_dictionary(self, dictionary: dict) -> FormPage:
        web_assert.is_true(self.contains_sub_dictionary(dictionary))
        return self

    def should_not_contain_sub_dictionary(self, dictionary: dict) -> FormPage:
        web_assert.is_false(self.contains_sub_dictionary(dictionary))
        return self

    def contains_sub_list(self, lst: list) -> bool:
        return bool(
            common.matching.matching_lists(
                self.table_text_list
            ).by_exact_list(lst)
        )

    def should_contain_sub_list(self, lst: list) -> FormPage:
        web_assert.is_true(self.contains_sub_list(lst))
        return self

    def should_have_text(self, text: str) -> FormPage:
        self.tbody.by(have.text(text)).should(have.size_greater_than_or_equal(1))
        return self

    def should_have_text_by_index(self, index: int, text: str) -> FormPage:
        self.tbody.element(index).should(have.text(text))
        return self

    def should_have_row_attribute(self, row_keyword: Union[str, list], attribute: str, value: str) -> FormPage:
        text = self.get_row_attribute_by_text(row_keyword, attribute)
        web_assert.is_equal(text, value)
        return self


class FormsPage(FormPage):
    check_next_page_enable_function: Callable = None

    next_page_button: Element = None
    page_index_button: Collection = None

    def with_traverse_all_pages(self, fn: Callable, *args, **kwargs):
        while True:
            res = fn(*args, **kwargs)
            if not self.check_and_click_next_page_button():
                break
        self.back_to_first_page()
        return res

    def check_and_click_next_page_button(self) -> bool:
        enabled = not self.check_next_page_enable_function(self.next_page_button)
        self.next_page_button.click() if enabled else ...
        time.sleep(0.5)
        return enabled

    def back_to_first_page(self) -> FormsPage:
        self.page_index_button.by(have.text('1')).element_by(be.clickable).click()
        time.sleep(0.5)
        return self

    def matching_elements_in_tables_by_row_keyword(self, row_keyword: Union[str, list]) -> Collection:
        while True:
            elements = self.matching_elements_in_table_by_row_keyword(row_keyword)
            if len(elements) > 0:
                break
            if not self.check_and_click_next_page_button():
                break
        return elements

    def get_table_all_info_with_dictionaries(self) -> List[Dict]:
        all_info = []
        self.with_traverse_all_pages(
            lambda val: val.extend(self.table_text_list),
            all_info
        )
        return common.convert.zip_dict(self.ths, *all_info)

    def get_table_all_info_with_lists(self) -> List[List]:
        all_info = []
        self.with_traverse_all_pages(
            lambda val: val.extend(self.table_text_list),
            all_info
        )
        return all_info

    def matching_dictionaries_in_table_by_dictionaries(
            self,
            origin_dictionaries: List[Dict],
            dictionaries: List[Dict],
            /
    ) -> List[Dict]:
        matched_list = []
        for dictionary in dictionaries:
            tmp = common.matching.matching_dictionaries(origin_dictionaries).by_exact_dictionary(dictionary)
            matched_list.extend(tmp) if tmp else ...
        return matched_list

    def matching_lists_in_table_by_lists(
            self,
            origin_lists: List[List],
            lists: List[List],
            /
    ) -> List[List]:
        matched_list = []
        for lst in lists:
            tmp = common.matching.matching_lists(origin_lists).by_exact_list(lst)
            matched_list.extend(tmp) if tmp else ...
        return matched_list

    def should_contain_sub_dictionaries(self, dictionaries: List[Dict]) -> List:
        matched_list = self.matching_dictionaries_in_table_by_dictionaries(
            self.get_table_all_info_with_dictionaries(),
            dictionaries
        )
        web_assert.is_equal(
            len(dictionaries),
            len(matched_list)
        )
        return matched_list

    def should_contain_sub_lists(self, lists: List[List]) -> List:
        matched_list = self.matching_lists_in_table_by_lists(
            self.get_table_all_info_with_lists(),
            lists
        )
        web_assert.is_equal(
            len(lists),
            len(matched_list)
        )
        return matched_list
