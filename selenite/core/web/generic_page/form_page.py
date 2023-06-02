from __future__ import annotations

import time
from typing import List, Union, Callable, Dict

from loguru import logger
from selene import Collection, by, query, have, be, Element

from selenite import common
from selenite.common.web_assert import web_assert


LOG_TAG = 'FORM_PAGE'


class Entity:
    thead: Collection = None
    tbody: Collection = None
    child: str = '*'

    @property
    def ths(self) -> List[str]:
        """
        Get table head text list
        """
        thead = [_.get(query.text) for _ in self.thead]
        logger.debug(f'[{LOG_TAG}] Form head is: {thead}')
        return thead

    @property
    def table_element_list(self) -> List[List[Element]]:
        """
        Get table element list
        """
        tbody_elements = [[_ for _ in row.all(by.xpath(self.child))] for row in self.tbody]
        logger.debug(f'[{LOG_TAG}] Form body is: {tbody_elements}')
        return tbody_elements

    @property
    def table_text_list(self) -> List[List[str]]:
        """
        Get table text list
        """
        i = self.table_element_list
        text_list = [[_.get(query.text) for _ in __] for __ in i]
        logger.debug(f'[{LOG_TAG}] Form body text is: {text_list}')
        return text_list

    @property
    def table_row_size(self) -> int:
        """
        Get table row size
        """
        size = len(self.tbody)
        logger.debug(f'[{LOG_TAG}] Form body row size is: {size}')
        return size

    def matching_elements_in_table_by_row_keyword(self, row_keyword: Union[str, list]) -> Collection:
        """
        Get matching elements in table by row keyword
        """
        elements = self.tbody
        for keyword in ([row_keyword] if isinstance(row_keyword, str) else row_keyword):
            elements = elements.by(have.text(keyword))
            if len(elements) == 0:
                break
        logger.debug(f'[{LOG_TAG}] Matching elements in table by row keyword: {row_keyword}')
        return elements


class FormPage(Entity):

    def get_row_attribute_by_index(self, index: int, attribute: str) -> str:
        """
        Get row attribute by index
        """
        i = self.ths.index(attribute)
        text = self.tbody.element(index).all(by.xpath(self.child)).element(i).get(query.text)
        logger.debug(f'[{LOG_TAG}] Get row attribute by index: {index}, attribute: {attribute}, text: {text}')
        return text

    def get_row_attribute_by_text(self, row_keyword: Union[str, list], attribute) -> str:
        """
        Get row attribute by text
        """
        i = self.ths.index(attribute)
        elements = self.matching_elements_in_table_by_row_keyword(row_keyword)
        text = (
            elements.element_by(be.visible).all(by.xpath(self.child)).element(i).get(query.text)
        ) if len(elements) else None
        logger.debug(f'[{LOG_TAG}] Get row attribute by text: {row_keyword}, attribute: {attribute}, text: {text}')
        return text

    def contains_sub_dictionary(self, dictionary: dict) -> bool:
        """
        Check if table contains sub dictionary
        """
        is_contain = bool(
            common.matching.matching_dictionaries(
                common.convert.zip_dict(
                    self.ths,
                    *self.table_text_list)
            ).by_exact_dictionary(dictionary)
        )
        logger.debug(f'[{LOG_TAG}] Contains sub dictionary: {dictionary}, result: {is_contain}')
        return is_contain

    def should_contain_sub_dictionary(self, dictionary: dict) -> FormPage:
        """
        Check if table should contain sub dictionary
        """
        logger.debug(f'[{LOG_TAG}] Should contain sub dictionary: {dictionary}')
        web_assert.is_true(self.contains_sub_dictionary(dictionary))
        return self

    def should_not_contain_sub_dictionary(self, dictionary: dict) -> FormPage:
        """
        Check if table should not contain sub dictionary
        """
        logger.debug(f'[{LOG_TAG}] Should not contain sub dictionary: {dictionary}')
        web_assert.is_false(self.contains_sub_dictionary(dictionary))
        return self

    def contains_sub_list(self, lst: list) -> bool:
        """
        Check if table contains sub list
        """
        is_contain = bool(
            common.matching.matching_lists(
                self.table_text_list
            ).by_exact_list(lst)
        )
        logger.debug(f'[{LOG_TAG}] Contains sub list: {lst}, result: {is_contain}')
        return is_contain

    def should_contain_sub_list(self, lst: list) -> FormPage:
        """
        Check if table should contain sub list
        """
        logger.debug(f'[{LOG_TAG}] Should contain sub list: {lst}')
        web_assert.is_true(self.contains_sub_list(lst))
        return self

    def should_have_text(self, text: str) -> FormPage:
        """
        Check if table should have text
        """
        logger.debug(f'[{LOG_TAG}] Should have text: {text}')
        self.tbody.by(have.text(text)).should(have.size_greater_than_or_equal(1))
        return self

    def should_have_text_by_index(self, index: int, text: str) -> FormPage:
        """
        Check if table should have text by index
        """
        logger.debug(f'[{LOG_TAG}] Should have text by index: {index}, text: {text}')
        self.tbody.element(index).should(have.text(text))
        return self

    def should_have_row_attribute(self, row_keyword: Union[str, list], attribute: str, value: str) -> FormPage:
        """
        Check if table should have row attribute
        """
        logger.debug(f'[{LOG_TAG}] Should have row attribute: {row_keyword}, attribute: {attribute}, value: {value}')
        text = self.get_row_attribute_by_text(row_keyword, attribute)
        web_assert.is_equal(text, value)
        return self


class FormsPage(FormPage):
    check_next_page_enable_function: Callable = None

    next_page_button: Element = None
    page_index_button: Collection = None

    def with_traverse_all_pages(self, fn: Callable, *args, **kwargs):
        """
        Traverse all pages
        """
        while True:
            res = fn(*args, **kwargs)
            if not self.check_and_click_next_page_button():
                logger.debug(f'[{LOG_TAG}] Traverse all pages done')
                break
        self.back_to_first_page()
        return res

    def check_and_click_next_page_button(self) -> bool:
        """
        Check and click next page button
        """
        logger.debug(f'[{LOG_TAG}] Check and click next page button')
        enabled = not self.check_next_page_enable_function(self.next_page_button)
        self.next_page_button.click() if enabled else ...
        time.sleep(0.5)
        return enabled

    def back_to_first_page(self) -> FormsPage:
        """
        Back to first page
        """
        logger.debug(f'[{LOG_TAG}] Back to first page')
        self.page_index_button.by(have.text('1')).element_by(be.clickable).click()
        time.sleep(0.5)
        return self

    def matching_elements_in_tables_by_row_keyword(self, row_keyword: Union[str, list]) -> Collection:
        """
        Matching elements in tables by row keyword
        """
        while True:
            elements = self.matching_elements_in_table_by_row_keyword(row_keyword)
            if len(elements) > 0:
                break
            if not self.check_and_click_next_page_button():
                break
        logger.debug(f'[{LOG_TAG}] Matching elements in tables by row keyword: {row_keyword}, elements: {elements}')
        return elements

    def get_table_all_info_with_dictionaries(self) -> List[Dict]:
        """
        Get table all info with dictionaries
        """
        all_info = []
        self.with_traverse_all_pages(
            lambda val: val.extend(self.table_text_list),
            all_info
        )
        table_all_info = common.convert.zip_dict(self.ths, *all_info)
        logger.debug(f'[{LOG_TAG}] Get table all info with dictionaries: {table_all_info}')
        return table_all_info

    def get_table_all_info_with_lists(self) -> List[List]:
        """
        Get table all info with lists
        """
        all_info = []
        self.with_traverse_all_pages(
            lambda val: val.extend(self.table_text_list),
            all_info
        )
        logger.debug(f'[{LOG_TAG}] Get table all info with lists: {all_info}')
        return all_info

    def matching_dictionaries_in_table_by_dictionaries(
            self,
            origin_dictionaries: List[Dict],
            dictionaries: List[Dict],
            /
    ) -> List[Dict]:
        """
        Matching dictionaries in table by dictionaries
        """
        matched_list = []
        for dictionary in dictionaries:
            tmp = common.matching.matching_dictionaries(origin_dictionaries).by_exact_dictionary(dictionary)
            matched_list.extend(tmp) if tmp else ...
        logger.debug(f'[{LOG_TAG}] Matching dictionaries in table by dictionaries: {dictionaries}, matched list: {matched_list}')
        return matched_list

    def matching_dictionaries_in_table_by_partial_dictionaries(
            self,
            origin_dictionaries: List[Dict],
            dictionaries: List[Dict],
            /
    ) -> List[Dict]:
        """
        Matching dictionaries in table by partial dictionaries
        """
        matched_list = []
        for dictionary in dictionaries:
            tmp = common.matching.matching_dictionaries(origin_dictionaries).by_partial_dictionary(dictionary)
            matched_list.extend(tmp) if tmp else ...
        logger.debug(f'[{LOG_TAG}] Matching dictionaries in table by dictionaries: {dictionaries}, matched list: {matched_list}')
        return matched_list

    def matching_lists_in_table_by_lists(
            self,
            origin_lists: List[List],
            lists: List[List],
            /
    ) -> List[List]:
        """
        Matching lists in table by lists
        """
        matched_list = []
        for lst in lists:
            tmp = common.matching.matching_lists(origin_lists).by_exact_list(lst)
            matched_list.extend(tmp) if tmp else ...
        logger.debug(f'[{LOG_TAG}] Matching lists in table by lists: {lists}, matched list: {matched_list}')
        return matched_list

    def matching_lists_in_table_by_partial_lists(
            self,
            origin_lists: List[List],
            lists: List[List],
            /
    ) -> List[List]:
        """
        Matching lists in table by partial lists
        """
        matched_list = []
        for lst in lists:
            tmp = common.matching.matching_lists(origin_lists).by_partial_list(lst)
            matched_list.extend(tmp) if tmp else ...
        logger.debug(f'[{LOG_TAG}] Matching lists in table by lists: {lists}, matched list: {matched_list}')
        return matched_list

    def should_contain_sub_dictionaries(self, dictionaries: List[Dict]) -> List:
        """
        Check if table should contain sub dictionaries
        """
        matched_list = self.matching_dictionaries_in_table_by_dictionaries(
            self.get_table_all_info_with_dictionaries(),
            dictionaries
        )
        logger.debug(f'[{LOG_TAG}] Should contain sub dictionaries: {dictionaries}, matched list: {matched_list}')
        web_assert.is_equal(
            len(dictionaries),
            len(matched_list)
        )
        return matched_list

    def should_contain_sub_partial_dictionaries(self, dictionaries: List[Dict]) -> List:
        """
        Check if table should contain sub partial dictionaries
        """
        matched_list = self.matching_dictionaries_in_table_by_partial_dictionaries(
            self.get_table_all_info_with_dictionaries(),
            dictionaries
        )
        logger.debug(f'[{LOG_TAG}] Should contain sub dictionaries: {dictionaries}, matched list: {matched_list}')
        web_assert.is_equal(
            len(dictionaries),
            len(matched_list)
        )
        return matched_list

    def should_contain_sub_lists(self, lists: List[List]) -> List:
        """
        Check if table should contain sub lists
        """
        matched_list = self.matching_lists_in_table_by_lists(
            self.get_table_all_info_with_lists(),
            lists
        )
        logger.debug(f'[{LOG_TAG}] Should contain sub lists: {lists}, matched list: {matched_list}')
        web_assert.is_equal(
            len(lists),
            len(matched_list)
        )
        return matched_list

    def should_contain_sub_partial_lists(self, lists: List[List]) -> List:
        """
        Check if table should contain sub partial lists
        """
        matched_list = self.matching_lists_in_table_by_partial_lists(
            self.get_table_all_info_with_lists(),
            lists
        )
        logger.debug(f'[{LOG_TAG}] Should contain sub lists: {lists}, matched list: {matched_list}')
        web_assert.is_equal(
            len(lists),
            len(matched_list)
        )
        return matched_list
