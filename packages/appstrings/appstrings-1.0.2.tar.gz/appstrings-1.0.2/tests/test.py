# ****************************************************************************
# @file test.py
#
# @author Ángel Fernández Pineda. Madrid. Spain.
# @date 2024-05-18
# @brief Translation utility
# @copyright 2024. Ángel Fernández Pineda. Madrid. Spain.
# @license Licensed under the EUPL
# *****************************************************************************

from appstrings import gettext,install,set_translation_locale,get_translation_locale,get_installed_translators,TranslatorException,_reset
from enum import Enum
from locale import getlocale

# *****************************************************************************
# Automated Test
# *****************************************************************************

if __name__ == "__main__":
    print("----------------------------------")
    print("appstrings: Automated test")
    print("----------------------------------")
    system_locale = get_translation_locale()
    print(f"Current language code: {system_locale}")

    class EN(Enum):
        _lang = "en"
        _desc = "for testing purposes"
        TEST = "English"

    class ES(Enum):
        _lang = "es"
        TEST = "Spanish"

    class ES_MX(Enum):
        _lang = "es_MX"
        TEST = "Spanish_Mexico"

    class Error1(Enum):
        TEST = "Not valid"

    class Error2(Enum):
        _lang = "pt"

    class EN2(Enum):
        _lang = "en"
        _domain = "test"
        TEST = "EN2"
        OTHER = "English"

    class ES2(Enum):
        _lang = "es"
        _domain = "test"
        TEST = "ES2"
        OTHER = "Spanish"

    print("Testing invalid translator installation")
    _reset()
    try:
        install(Error1)
        print("Failure: Class Error1 should not install")
    except TranslatorException:
        pass

    _reset()
    try:
        install(EN)
        install(Error2)
        print("Failure: Class Error2 should not install")
    except TranslatorException:
        pass

    print("Done")

    print("Testing no default translator")
    _reset()

    try:
        t = gettext(EN.TEST)
        if t != EN.TEST._value_:
            print("Failure at EN.TEST")
        t = gettext(ES.TEST)
        if t != ES.TEST._value_:
            print("Failure at ES.TEST")
    except TranslatorException:
        print("Failure due to exception")
    print("Done")

    print("Testing current translation language")
    _reset()
    set_translation_locale("en")
    l = get_translation_locale()
    if l != "en":
        print("Failure: 'en' was not set as current language")

    set_translation_locale("en_US")
    l = get_translation_locale()
    if l != "en_US":
        print("Failure: 'en_US' was not set as current locale")

    set_translation_locale("PT")
    l = get_translation_locale()
    if l != "pt":
        print("Failure: 'PT' was not set as current language")

    set_translation_locale()
    if get_translation_locale() != system_locale:
        print("Failure: system locale not set")
    print("Done")

    print("Test translation #1")
    _reset()
    set_translation_locale("en")
    install(ES)
    install(EN)
    t = gettext(ES.TEST)
    if t != EN.TEST._value_:
        print("Failure")
    print("Done")

    print("Test translation #2")
    _reset()
    set_translation_locale("pt")
    install(ES)
    install(EN)
    t = gettext(EN.TEST)
    if t != EN.TEST._value_:
        print("Failure")
    print("Done")

    print("Test translation #3")
    _reset()
    set_translation_locale("es_MX")
    install(ES)
    install(EN)
    t = gettext(ES.TEST)
    if t != ES.TEST._value_:
        print("Failure")
    print("Done")

    print("Test translation #4")
    _reset()
    set_translation_locale("es_MX")
    install(ES)
    install(ES_MX)
    t = gettext(ES.TEST)
    if t != ES_MX.TEST._value_:
        print("Failure")
    print("Done")

    print("Test translation #5")
    _reset()
    install(EN)
    install(ES_MX)
    set_translation_locale("es_MX")
    t = gettext(EN.TEST)
    if t != ES_MX.TEST._value_:
        print("Failure")
    print("Done")
    # Do not call _reset() for the following test
    print("Test translation #6")
    set_translation_locale("en_US")
    t = gettext(ES_MX.TEST)
    if t != EN.TEST._value_:
        print("Failure")

    print("Done")

    print("Testing installation of translators in different domains")
    try:
        install(EN)
        install(EN2)
        install(ES2)
    except TranslatorException:
        print("Failure")
    print("Done")

    print("Testing enumeration of installed translators")
    _reset()
    install(EN)
    install(ES)
    install(ES_MX)
    install(EN2)
    install(ES2)
    print(f" Domain: {__name__}")
    l = [x._lang._value_ for x in get_installed_translators(__name__)]
    l.sort()
    if l != ["en","es","es_MX"]:
        print("Failure.")
        print(f"Found: {l}")
    print(" Domain: test")
    l = [x._lang._value_ for x in get_installed_translators(EN2._domain._value_)]
    if l != ["en","es"]:
        print("Failure.")
        print(f"Found: {l}")
    print("Done")

    print("Testing translation in different domains")
    _reset()
    install(EN)
    install(ES2)
    set_translation_locale("es")
    if gettext(EN.TEST) != EN.TEST._value_:
        print("Failure #1.")
    if gettext(EN2.TEST) != ES2.TEST._value_:
        print("Failure #2.")
    print("Done")

    print("----------------------------------")
