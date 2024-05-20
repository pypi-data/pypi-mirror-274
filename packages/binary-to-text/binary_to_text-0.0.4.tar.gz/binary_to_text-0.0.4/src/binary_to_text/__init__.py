"""

:authors: Muka
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2021 Muka
"""

from .main import BinaryTranslator

_translator = BinaryTranslator()

def binary_to_text(binary_code):
    return _translator.binary_to_text(binary_code)

def text_to_binary(text):
    return _translator.text_to_binary(text)