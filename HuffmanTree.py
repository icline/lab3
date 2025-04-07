import heapq
from collections import namedtuple, Counter

class HuffmanTree:
    """
    Encodes and decodes strings using Huffman Tree encoding.

    Attributes:
        - chars: List of characters to be encoded
        - freqs: List containing the frequency of each character
    """

    class Node:
        """
        A node to be inserted in the Huffman Encoding Tree.

        Each node contains a character with a corresponding frequency as well as a left and right pointer

        Attributes:
            - char: A character
            - freq: Frequency of the corresponding character
            - left: Node's left pointer
            - right: Node's right pointer
        """
        
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # Defines the Precedence
        def __lt__(self, other):
            if self.freq == other.freq and len(self.char) == len(other.char):
                return ord(self.char.lower()) < ord(other.char.lower())
            elif self.freq == other.freq:
                return len(self.char) < len(other.char)
            return self.freq < other.freq
        
    def __init__(self, chars, freqs):
        self.chars = chars
        self.freqs = freqs 

    class ErrorHandling:
    
        class InvalidCharacterError(Exception):
            pass
    
        class DuplicateCharacterError(Exception):
            pass
    
        class ZeroOrNegativeFrequencyError(Exception):
            pass
    
        class InvalidHuffmanTreeError(Exception):
            pass
    
        def __init__(self):
            self.response = namedtuple('Response', ['valid', 'error'], defaults=[True, None])

        def check_huffman_tree(self, root):
            """Check if the Huffman tree is valid (not None)."""
            if root is None:
                raise self.InvalidHuffmanTreeError("Error: The Huffman tree is empty or not built correctly.")
            return True

        def check_for_invalid_characters(self, frequencies):
            """Ensure all characters in the frequency table are valid."""
            for char in frequencies:
                if not char.isalpha() or len(char) != 1:
                    raise self.InvalidCharacterError(f"Invalid character '{char}' found in the frequency table.")
    
        def check_for_duplicate_characters(self, frequencies):
            """Ensure all characters in the frequency table are unique."""
            seen = set()
            for char in frequencies:
                if char in seen:
                    raise self.DuplicateCharacterError(f"Duplicate character '{char}' found in the frequency table.")
                seen.add(char)
    
        def check_for_zero_or_negative_frequencies(self, frequencies):
            """Ensure all frequencies are positive integers."""
            for char, freq in frequencies.items():
                if freq <= 0:
                    raise self.ZeroOrNegativeFrequencyError(f"Invalid frequency {freq} for character '{char}'. Frequencies must be positive.")
    
        def validate_frequency_table(self, frequencies):
            """Validate the frequency table for correct characters and frequencies."""
            self.check_for_invalid_characters(frequencies)
            self.check_for_duplicate_characters(frequencies)
            self.check_for_zero_or_negative_frequencies(frequencies)

    def build_huffman_tree(self):
        """Builds a Huffman Tree."""
        frequencies = dict(zip(self.chars, self.freqs))
        error_handler = self.ErrorHandling()

        error_handler.validate_frequency_table(frequencies)
    
        # Build the priority queue and the Huffman tree
        priority_queue = [self.Node(self.chars[i], self.freqs[i]) for i in range(len(self.chars))]
        heapq.heapify(priority_queue)
    
        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            combined = self.Node(left.char + right.char, left.freq + right.freq)
            combined.left = left
            combined.right = right
            heapq.heappush(priority_queue, combined)
    
        root = priority_queue[0]
        error_handler.check_huffman_tree(root)
    
        # Return the root node of the Huffman tree
        return root

    # def print_huffman_tree(self, node, indent="", branch=""):
    #     if node is None:
    #         return
        
    #     print(indent+branch, end="")
    #     if node.char is not None:
    #         print(f'{node.char}: {node.freq}')
    
    #     indent += "    "
    #     self.print_huffman_tree(node.left, indent, "Left: ")
    #     self.print_huffman_tree(node.right, indent, "Right: ")

    def print_preorder_traversal(self, node):
        """Prints the tree using preorder traversal as required by the lab."""
        result = []
        self._preorder_recursive(node, result)
        print("The tree in preorder is:", ", ".join(result))

    def _preorder_recursive(self, node, result):
        """
        Helper method for recursive preorder traversal.
        Visits nodes in order: root, left subtree, right subtree.
        """
        if node is None:
            return

        # Visit root
        result.append(f"{node.char}: {node.freq}")

        # Visit left subtree
        self._preorder_recursive(node.left, result)

        # Visit right subtree
        self._preorder_recursive(node.right, result)

    # def get_codes(self, node, code=""):
    #     if node is None:
    #         return

    #     if node.char is not None and len(node.char) == 1:
    #         print(f'{node.char} = {code}')
        
    #     self.get_codes(node.left, code + '0')
    #     self.get_codes(node.right, code + '1')

    def get_codes_dict(self, node, code="", code_map=None):
        """Gets all of the character codes and stores them in a dictionary."""
        if code_map is None:
            code_map = {}

        if node is None:
            return code_map

        if node.char is not None and len(node.char) == 1:
            code_map[code] = node.char  # Reverse mapping: code -> char

        self.get_codes_dict(node.left, code + '0', code_map)
        self.get_codes_dict(node.right, code + '1', code_map)

        return code_map
    
    # def generate_codes(self, node=None, current_code="", codes=None):
    #     # Initialize on first call
    #     if node is None:
    #         node = self.root
    #         codes = {}

    #     # Base case: if at a leaf node, assign the code
    #     if node.char is not None:
    #         codes[node.char] = current_code if current_code else "0"
    #         return codes

    #     # Recursively traverse left and right children
    #     if node.left:
    #         self.generate_codes(node.left, current_code + "0", codes)
    #     if node.right:
    #         self.generate_codes(node.right, current_code + "1", codes)

    #     return codes
'''
if __name__ == "__main__":
    chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    freqs = [19, 16, 17, 11, 42, 12, 14, 17, 16, 5, 10, 20, 19, 24, 18, 13, 1, 25, 35, 25, 15, 5, 21, 2, 8, 3]

    tree = HuffmanTree(chars, freqs)
    root = tree.huffman_tree()

    codes_dict = tree.get_codes_dict(root)

    print("\nHuffman Dictionary (Code -> Letter):")
    for code, char in codes_dict.items():
        print(f"{code}: {char}")
    
    #tree.get_codes(root)

'''