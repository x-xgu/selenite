from __future__ import annotations

import re
from typing import List, Dict


class MatchingDictionaries:
    """
    A class to match dictionaries by exact or partial match.
    """
    def __init__(self, dictionaries: List[Dict]):
        self._dictionaries = dictionaries

    def by_exact_dictionary(self, exact_dictionary: Dict) -> List[Dict]:
        """
        Returns a list of dictionaries that match the exact dictionary.
        """
        return [
            d for d in self._dictionaries
            if all(
                d.get(key) == value
                for key, value
                in exact_dictionary.items()
            )
        ]

    def by_partial_dictionary(self, partial_dictionary: Dict) -> List[Dict]:
        """
        Returns a list of dictionaries that match the partial dictionary.
        """
        patterns = {
            key: re.compile(pattern)
            for key, pattern in partial_dictionary.items()
        }
        return [
            d for d in self._dictionaries
            if all(
                patterns[key].search(d[key])
                for key in partial_dictionary
            )
        ]


class MatchingLists:
    """
    A class to match lists by exact or partial match.
    """
    def __init__(self, lists: List[List]):
        self._lists = lists

    def by_exact_list(self, exact_list: List) -> List[List]:
        """
        Returns a list of lists that match the exact list.
        """
        return [
            _ for _ in self._lists
            if all(
                item in _
                for item in exact_list
            )
        ]

    def by_partial_list(self, partial_list: List) -> List[List]:
        """
        Returns a list of lists that match the partial list.
        """
        regex_list = [
            re.compile(pattern)
            if isinstance(pattern, str) else pattern
            for pattern in partial_list
        ]
        return [
            _ for _ in self._lists
            if all(
                regex.search(str(elem))
                for regex, elem in zip(regex_list, _)
            )
        ]


def matching_dictionaries(dictionaries: List[Dict]) -> MatchingDictionaries:
    """
    Matches dictionaries by exact or partial match.
    """
    return MatchingDictionaries(dictionaries)


def matching_lists(lists: List[List]) -> MatchingLists:
    """
    Matches lists by exact or partial match.
    """
    return MatchingLists(lists)
