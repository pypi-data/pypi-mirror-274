"""
Short useful text functions library
"""
import re
from typing import (Optional,
                    Union
                    )
from loguru import logger

from ownlib.months import months_df

SPACE_CHAR: str = ' '
TAB_CHAR = '\t'
NEW_LINE = '\n'
EMPTY_STR = ''

complete_rules = {'\xa0': EMPTY_STR,
                  '\n': SPACE_CHAR
                  }
# noAutoStringLength = 10


def nominative_month(month_mame: str) -> str | None:
    """
    TODO Add some description
    """
    return (month_mame[:-1] + 'й' if month_mame.lower() == 'мая'
            else month_mame[:-1] + 'ь' if month_mame[-1:] == 'я'
            else month_mame[:-1] if month_mame[-1:] == 'а'
            else None
            )


def translated_month(month: str) -> str | None:
    """
    TODO Add some description
    """
    # TODO make mirroring language functionality (ru->lat, lat->ru) \
    #  (?) auto lang recognition
    try:
        translated = months_df[months_df['russian']
                               == month]['english'].values[0]
    except IndexError as ie_ex:
        logger.exception('Wrong argument: ', month)
        raise ie_ex

    return translated


def get_month_number(month: str) -> int | None:
    """
    TODO Add some description
    """
    try:
        month_number = months_df[months_df['english'] == month]['number'].values[0]
    except IndexError:
        logger.exception('Wrong argument: ', month)
        month_number = None

    return int(month_number)


def cyrillic_in(arg: str) -> bool:
    """
    TODO Add some description
    """
    return bool(re.search(r'([а-яА-ЯёЁ]\w+)', arg))


def lat_in(arg: str) -> bool:
    """
    TODO Add some description
    """
    return bool(re.search(r'([a-zA-Z]\w+)', arg))


def digit_in(arg: str) -> bool:
    """
    TODO Add some description
    """
    return bool(re.search(r'\d', arg))


def pattern_only(arg: str, pattern: str) -> bool:
    """
    TODO Add some description
    """
    return arg == EMPTY_STR.join(re.findall(pattern, arg))


def cyrillic_only(arg: str) -> bool:
    """
    TODO Add some description
    """
    return pattern_only(arg, r'[а-яА-ЯёЁ]')


def lat_only(arg: str) -> bool:
    """
    TODO Add some description
    """
    return pattern_only(arg, r'[a-zA-Z]')


def digit_only(arg: str) -> bool:
    """
    TODO Add some description
    """
    return pattern_only(arg, r'[0-9]')
    # return arg == EMPTY_STR.join(re.findall(pattern, arg))


def get_month(month_field: str) -> str:
    """
    TODO Add some description
    """
    if cyrillic_only(month_field):
        # FIXME Понять как обрабатывать ошибку аргумента
        month_field = nominative_month(month_field).title()
        month_field = translated_month(month_field)
    elif not lat_only(month_field):
        month_field = 'MonthParsingError'

    return month_field


def string_transform(manipulated_string: str,
                     rules: dict[str, str] | None = None) -> str | None:
    """Change change_rules.key => change_rules.value in manipulated_string

    :param manipulated_string: str - source string on which we could change a symbols
    # TODO Have change to ordered dict type
    :param rules: dict - {symbol_from_change : symbol_to_change}
    :return: result string: str
    Example rules: rules = {'\xa0' : EMPTY_STR, '\n' : ' '}
    """
    result_string = ''
    # Leave here default value setting else catch default mutable warning in func arg line
    rules = rules if rules else {'\xa0': EMPTY_STR}

    # TODO use str.replace() here, but with type(rules) == OrderedDict
    for char in manipulated_string:
        result_string += rules[char] \
            if char in rules else char
    return result_string


def list_transform(manipulated_list: list[str],
                   change_rules: Optional[dict[str, str]] = None):
    """
    Change change_rules.key => change_rules.value in manipulated_list
    
    :param manipulated_list: list - source list on which we could change a symbols
    :param change_rules: dict - {symbol_from_change : symbol_to_change} \
    Example: {'\xa0':'', '\n':' '}
    :return: result list: list
    """
    # TODO Though about union both of this functions ^
    if change_rules is None:
        change_rules = {'\xa0': EMPTY_STR}
    return [string_transform(string, change_rules) for string in manipulated_list]


def txt2float(arg: str) -> float | None:
    """
    Convert  str -> float. Change ',' -> '.', '\xa0' -> ''
    
    :param arg: str - string via digits
    :return: float(arg)
    """
    arg = arg.replace(',', '.')
    arg = arg.replace("\xa0", EMPTY_STR)

    try:
        float_arg = float(arg)
    except ValueError:
        logger.exception('Wrong argument format', arg)
        float_arg = None

    return float_arg


def items_in_string(analysing_string: str,
                    parent_list: list[str]) -> list[str]:
    """
    Return the ordered list of words from analysing string,
    # TODO Rename variables Idea - 'patterns'
    which have equals in the predefined list

    :param analysing_string: str - Analysing string
    :param parent_list: list[str] - Predefined list
    :return: list[str] - An ordered list of words equals the same
    ones in parent_list
    """
    return [item[0] for item in [[value for value in parent_list
                                  if value == word]
                                 for word in analysing_string.split()]
            if item]
