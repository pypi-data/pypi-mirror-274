from binary_to_text import binary_to_text, text_to_binary

binary_code = '01001000 01100101 01101100 01101100 01101111'
text = binary_to_text(binary_code)
print(f"Translation of binary code '{binary_code}' to text: '{text}'")

text = 'Hello'
binary_code = text_to_binary(text)
print(f"Translation of text '{text}' to binary code: '{binary_code}'")