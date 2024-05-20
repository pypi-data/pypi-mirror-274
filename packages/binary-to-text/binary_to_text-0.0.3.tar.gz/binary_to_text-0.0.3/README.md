
Hello this is my first library this library converts binary code into text and vice versa
----------

Converts a string of binary code to text
----------
    binary_to_text(binary_code)

Converts a string of text to binary code
----------
    text_to_binary(text)
Usage example
----------
Binary code to text

    binary_code = '01001000 01100101 01101100 01101100 01101111'
    text = binary_to_text(binary_code)
    print(f"Translation of binary code '{binary_code}' to text: '{text}'")

Text to binary code

    text = 'Hello'
    binary_code = text_to_binary(text)
    print(f"Translation of text '{text}' to binary code: '{binary_code}'")