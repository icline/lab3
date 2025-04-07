import re
from HuffmanTree import HuffmanTree

class ErrorHandling:
    def response(self, valid, message):
        return {'valid': valid, 'message': message}

    def validate_huffman_input(self, encoded_string):
        if not encoded_string:
            return self.response(False, "Error: The encoded string is empty.")
        
        for bit in encoded_string:
            if bit not in {'0', '1'}:
                return self.response(False, "Error: The encoded string contains non-binary characters.")
        
        return self.response(True, None)
    
    def remove_spaces(self, string):
        return string.replace(" ", "")
    
    def keep_only_letters(self, text):
        filtered = re.sub(r'[^A-Za-z]', '', text)
        return filtered

class HuffmanCoder:
    def __init__(self, huffman_codes):
        self.huffman_codes = huffman_codes
        self.error_handler = ErrorHandling()

    def decode(self, data):
        data = self.error_handler.remove_spaces(data)
        validation = self.error_handler.validate_huffman_input(data)

        if not validation["valid"]:
            print(validation["message"])
            return ""

        result = ""
        start_index = 0
        max_index = len(data)

        while start_index < max_index:
            for length in range(1, max_index - start_index + 1):
                substring = data[start_index:start_index + length]

                if substring in self.huffman_codes:
                    result += self.huffman_codes[substring]
                    start_index += length
                    break
            else:
                print(self.error_handler.response(False, f"No match found. Decoding stopped."))
                return None

        return result

    def encode(self, input_string):
        cleaned_input = self.error_handler.remove_spaces(input_string)
        cleaned_input = self.error_handler.keep_only_letters(cleaned_input.upper())

        if not cleaned_input:
            print(self.error_handler.response(False, "Error: No valid letters in input to encode."))
            return None

        result = ""
        for char in cleaned_input:
            found = False
            for code, letter in self.huffman_codes.items():
                if letter == char:
                    result += code
                    found = True
                    break
            if not found:
                print(self.error_handler.response(False, f"Match not found in Huffman codes."))

        return result

'''
chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
freqs = [19, 16, 17, 11, 42, 12, 14, 17, 16, 5, 10, 20, 19, 24, 18, 13, 1, 25, 35, 25, 15, 5, 21, 2, 8, 3]

tree = HuffmanTree(chars, freqs)
root = tree.huffman_tree()
code_dict = tree.get_codes_dict(root)

coder = HuffmanCoder(code_dict)

#TESTING ONLY
encoded_string = '0110011111100111111'

decoded_string = coder.decode(encoded_string)
print(f"Decoded string: {decoded_string}")

encoded_string = coder.encode(decoded_string)
print(f"Encoded string: {encoded_string}")
'''