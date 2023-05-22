from __future__ import annotations

import re
from typing import List, Dict


def matching_dictionaries(dictionaries: List[Dict[str, str]]) -> 'Matching':
    """
    Returns an instance of Matching class for dictionaries.

    Args:
        dictionaries: A list of dictionaries.

    Returns:
        Matching: An instance of Matching class for dictionaries.

    Example:
        >>> dictionaries = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
        >>> matching = matching_dictionaries(dictionaries)
        >>> matching.exact_dictionary({'name': 'John'})
        [{'name': 'John', 'age': '30'}]
    """
    class Matching:
        """
        Matching class for dictionaries.
        """

        def __init__(self, dictionaries: List[Dict[str, str]]):
            self._dictionaries = dictionaries

        def exact_dictionary(self, exact_dictionary: Dict[str, str]) -> List[Dict[str, str]]:
            """
            Returns a list of dictionaries that exactly match the given dictionary.

            Args:
                exact_dictionary: A dictionary to be matched exactly.

            Returns:
                List[Dict[str, str]]: A list of dictionaries that exactly match the given dictionary.

            Example:
                >>> dictionaries = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
                >>> matching = Matching(dictionaries)
                >>> matching.exact_dictionary({'name': 'John'})
                [{'name': 'John', 'age': '30'}]
            """
            return [
                d
                for d in self._dictionaries
                if all(
                    d.get(key) == value
                    for key, value
                    in exact_dictionary.items()
                )
            ]

        def partial_dictionary(self, partial_dictionary: Dict[str, str]) -> List[Dict[str, str]]:
            """
            Returns a list of dictionaries that partially match the given dictionary.

            Args:
                partial_dictionary: A dictionary to be partially matched.

            Returns:
                List[Dict[str, str]]: A list of dictionaries that partially match the given dictionary.

            Example:
                >>> dictionaries = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
                >>> matching = Matching(dictionaries)
                >>> matching.partial_dictionary({'name': 'Jo'})
                [{'name': 'John', 'age': '30'}]
            """
            patterns = {
                key: re.compile(pattern)
                for key, pattern
                in partial_dictionary.items()
            }
            return [
                d
                for d in self._dictionaries
                if all(
                    patterns[key].search(d[key])
                    for key
                    in partial_dictionary
                )
            ]

    return Matching(dictionaries)


def matching_lists(lists: List[List]) -> 'Matching':
    """
    Returns an instance of Matching class for lists.

    Args:
        lists: A list of lists.

    Returns:
        Matching: An instance of Matching class for lists.

    Example:
        >>> lists = [[1, 2, 3], [4, 5, 6]]
        >>> matching = matching_lists(lists)
        >>> matching.exact_list([1, 2])
        [[1, 2, 3]]
    """
    class Matching:
        """
        Matching class for lists.
        """

        def __init__(self, lists: List[List]):
            self._lists = lists

        def exact_list(self, exact_list: List) -> List[List]:
            """
            Returns a list of lists that exactly match the given list.

            Args:
                exact_list: A list to be matched exactly.

            Returns:
                List[List]: A list of lists that exactly match the given list.

            Example:
                >>> lists = [[1, 2, 3], [4, 5, 6]]
                >>> matching = Matching(lists)
                >>> matching.exact_list([1, 2])
                [[1, 2, 3]]
            """
            return [
                l_
                for l_
                in self._lists
                if all(
                    item in l_
                    for item
                    in exact_list
                )
            ]

        def partial_list(self, partial_list: List) -> List[List]:
            """
            Returns a list of lists that partially match the given list.

            Args:
                partial_list: A list to be partially matched.

            Returns:
                List[List]: A list of lists that partially match the given list.

            Example:
                >>> lists = [[1, 2, 3], [4, 5, 6]]
                >>> matching = Matching(lists)
                >>> matching.partial_list([re.compile('1'), 2])
                [[1, 2, 3]]
            """
            regex_list = [
                re.compile(pattern)
                if isinstance(pattern, str)
                else pattern
                for pattern
                in partial_list
            ]
            return [
                l_
                for l_
                in self._lists
                if all(
                    regex.search(str(elem))
                    for regex, elem
                    in zip(regex_list, l_)
                )
            ]

    return Matching(lists)
