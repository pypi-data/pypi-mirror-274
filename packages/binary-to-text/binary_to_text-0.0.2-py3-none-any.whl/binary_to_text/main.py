def greeting():
   return "Hello, I'm your first library!"


def binary_to_text(self, binary_string):
    """
    Переводит строку двоичного кода в текст.

    :param binary_string: Строка двоичного кода (например, '01001000 01100101 01101100 01101100 01101111')
    :return: Текстовое представление двоичного кода (например, 'Hello')
    """
    binary_values = binary_string.split()
    ascii_characters = [chr(int(bv, 2)) for bv in binary_values]
    return ''.join(ascii_characters)


def text_to_binary(self, text):
    """
    Переводит текст в строку двоичного кода.

    :param text: Текст (например, 'Hello')
    :return: Строка двоичного кода (например, '01001000 01100101 01101100 01101100 01101111')
    """
    binary_values = [format(ord(char), '08b') for char in text]
    return ' '.join(binary_values)