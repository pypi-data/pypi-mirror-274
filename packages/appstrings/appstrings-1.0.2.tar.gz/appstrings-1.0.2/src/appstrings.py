# ****************************************************************************
# @file appstrings.py
#
# @author Ángel Fernández Pineda. Madrid. Spain.
# @date 2024-01-22
# @brief Translation utility
# @copyright 2024. Ángel Fernández Pineda. Madrid. Spain.
# @license Licensed under the EUPL
# *****************************************************************************

"""
Minimal strings translation library for Python

This is not a full internationalization library,
nor suitable for usual translation workflows.
Make sure it meets your needs.

Functions:
    gettext(): Returns a translated string
    install(): Install an enumeration as a translator
    set_translation_locale(): Set a locale for translation
    get_translation_locale(): Get current locale used for translation
    get_installed_translators(): Retrieve a list of all installed translators


Exceptions:
    TranslatorException: for invalid language translators

"""

# *****************************************************************************
# "Exports"
# *****************************************************************************

__all__ = [
    "gettext",
    "install",
    "set_translation_locale",
    "get_translation_locale",
    "get_installed_translators",
    "TranslatorException"
]

# *****************************************************************************
# Imports
# *****************************************************************************

from enum import Enum
from _locale import _getdefaultlocale

# *****************************************************************************
# "private" global variables
# *****************************************************************************

__translators = {}
__current_translator = {}
__first_call = True

# *****************************************************************************
# Classes
# *****************************************************************************


class TranslatorException(Exception):
    """Exception for invalid language translators"""

    pass


# *****************************************************************************
# "private" functions
# *****************************************************************************


def _decode_locale(locale: str) -> tuple[str, str]:
    underscore_pos =locale.find("_")
    if (underscore_pos<0):
        return (locale.lower(),"")
    else:
        return (locale[:underscore_pos].lower(), locale[(underscore_pos+1):].lower())

def _reset():
    """(Re)initialize appstrings library for testing purposes
    """
    global __current_locale
    global __translators
    global __current_translator
    global __first_call
    __current_locale = _decode_locale(_getdefaultlocale()[0])
    __translators = {}
    __current_translator = {}
    __first_call = True


def _match_installed_translator(
    domain: str, current_lang: str, current_country: str
) -> Enum:
    result = None
    global __translators
    translator_list = __translators[domain]
    for translator in translator_list:
        translator_locale = _decode_locale(translator._lang._value_)
        translator_lang = translator_locale[0]
        translator_country = translator_locale[1]
        if translator_lang == current_lang:
            if translator_country == current_country:
                result = translator
                break
            if (translator_country == "") or (not result):
                result = translator
    return result


def __initialize():
    global __first_call
    global __current_translator
    global __current_locale
    __first_call = False
    if not __current_locale:
        raise TranslatorException("Current locale is unknown")
    current_lang = __current_locale[0]
    current_country = __current_locale[1]
    for domain in __translators.keys():
        translator = _match_installed_translator(domain, current_lang, current_country)
        __current_translator[domain] = translator


def __check_string_ids(cls1: Enum, cls2: Enum):
    if cls1 != cls2:
        for id in cls1:
            attr_name = id._name_
            if (attr_name[0] != "_") and (not hasattr(cls2, attr_name)):
                raise TranslatorException(
                    f"String ID '{attr_name}' from '{cls1.__name__}' is missing at '{cls2.__name__}'"
                )
        for id in cls2:
            attr_name = id._name_
            if (attr_name[0] != "_") and (not hasattr(cls1, attr_name)):
                raise TranslatorException(
                    f"String ID '{attr_name}' from '{cls2.__name__}' is missing at '{cls1.__name__}'"
                )


# *****************************************************************************
# "public" functions
# *****************************************************************************


def gettext(id) -> str:
    """Return a translated string

    The best-matching translator for the selected locale is used.

    Args:
        id (Enumeration attribute): Identifier of the string to translate

    Returns:
        str: Translated string
    """
    global __current_translator
    global __first_call
    if __first_call:
        __initialize()
    domain = (
        id.__class__._domain._value_
        if hasattr(id.__class__, "_domain")
        else id.__class__.__module__
    )
    if (domain in __current_translator) and __current_translator[domain]:
        return getattr(__current_translator[domain], id._name_)._value_
    else:
        return id._value_


def install(translator: Enum):
    """Install an enumeration as a translator

    Args:
        translator (Enum): An enumeration to work as a translator.
                           Must define a "_lang" attribute containing
                           a locale string or language string. For example:
                           "en" or "en_US". Should also define a "_domain"
                           attribute containing an application-specific
                           identifier (as a string).

    Raises:
        TranslatorException: The given translator is not valid
    """
    global __translators
    global __first_call
    __first_call = True
    if not hasattr(translator, "_lang"):
        raise TranslatorException(
            f"{translator.__name__} is missing the '_lang' attribute"
        )
    _decode_locale(translator._lang._value_)
    domain = (
        translator._domain._value_
        if hasattr(translator, "_domain")
        else translator.__module__
    )
    if domain not in __translators:
        __translators[domain] = []
    if translator not in __translators[domain]:
        if len(__translators[domain]) > 0:
            __check_string_ids(translator, __translators[domain][0])
        __translators[domain].append(translator)


def set_translation_locale(locale_str: str = None):
    """Set a locale for translation

    Args:
        locale_str (str): A locale string. For example, "en_US".
                          If not given, system locale is used.

    Remarks:
        Not mandatory. If not called, current system locale is used.
    """
    global __current_locale
    global __first_call
    __current_locale = _decode_locale(locale_str if locale_str else _getdefaultlocale()[0])
    __first_call = True


def get_translation_locale() -> str:
    """Get current locale used for translation

    Returns:
        str: Locale string
    """
    if __current_locale:
        result = __current_locale[0]
        locale_country = __current_locale[1]
        if locale_country != "":
            result += "_"
            result += locale_country.upper()
    else:
        result = ""
    return result


def get_installed_translators(domain: str) -> list:
    """Retrieve a list of all installed translators

    Args:
        domain (str): The domain of your application

    Returns:
        list: All translators for the given domain or
              an empty list if the given domain is unknown.
    """
    global __translators
    if domain in __translators:
        return __translators[domain].copy()
    else:
        return []


# *****************************************************************************
# Initialization
# *****************************************************************************

_reset()
