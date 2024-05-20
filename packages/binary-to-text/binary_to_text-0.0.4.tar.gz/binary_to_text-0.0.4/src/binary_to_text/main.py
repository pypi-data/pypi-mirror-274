class BinaryTranslator:
    def __init__(self):
        pass

    def binary_to_text(self, binary_code):
        binary_values = binary_code.split(' ')
        ascii_characters = [chr(int(bv, 2)) for bv in binary_values]
        return ''.join(ascii_characters)

    def text_to_binary(self, text):
        binary_values = [format(ord(char), '08b') for char in text]
        return ' '.join(binary_values)