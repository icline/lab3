import heapq

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
        
        def __init__(self, char=None, freq=None):
            self.char=char
            self.freq=freq
            self.left=None
            self.right=None

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

    def huffman_tree(self) -> Node:
        """Builds a Huffman Tree."""
        priority_queue=[self.Node(self.chars[i], self.freqs[i]) for i in range(len(self.chars))]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)

            combined = self.Node(left.char+right.char, left.freq + right.freq)
            combined.left = left
            combined.right = right
            heapq.heappush(priority_queue, combined)

        return priority_queue[0]
    
    # FOR TESTING
    # This function is just to test whether the Huffman Tree 
    # is built correctly. This function is not needed for the
    # final code, and can be removed.
    def print_huffman_tree(self, node, indent="", branch=""):
        """Prints the Huffman Tree (non-preorder traversal)."""
        if node is None:
            return
        
        print(indent+branch, end="")
        if node.char is not None:
            print(f'{node.char}: {node.freq}')
    
        indent += "    "
        self.print_huffman_tree(node.left, indent, "Left: ")
        self.print_huffman_tree(node.right, indent, "Right: ")

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

    def get_codes(self, node, code=""):
        """Prints all the character codes from the Huffman Tree."""
        if node is None:
            return

        if node.char is not None and len(node.char) == 1:
            print(f'{node.char} = {code}')
        
        self.get_codes(node.left, code + '0')
        self.get_codes(node.right, code + '1')

if __name__ == "__main__":
    chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    freqs = [19, 16, 17, 11, 42, 12, 14, 17, 16, 5, 10, 20, 19, 24, 18, 13, 1, 25, 35, 25, 15, 5, 21, 2, 8, 3]
    tree = HuffmanTree(chars, freqs)
    root = tree.huffman_tree()
    tree.get_codes(root)
    tree.print_preorder_traversal(root)



