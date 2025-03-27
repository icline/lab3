import heapq

class HuffmanTree:

    class Node:
        
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

    def huffman_tree(self):
        priority_queue=[self.Node(self.chars[i], self.freqs[i]) for i in range(len(self.chars))]
        heapq.heapify(priority_queue)

        # for node in priority_queue:
        #     print(f'{node.char}: {node.freq}')

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
        if node is None:
            return
        
        print(indent+branch, end="")
        if node.char is not None:
            print(f'{node.char}: {node.freq}')
    
        indent += "    "
        self.print_huffman_tree(node.left, indent, "Left: ")
        self.print_huffman_tree(node.right, indent, "Right: ")

    def preorder_traversal(self, node):
        if node is not None:
            print(f'{node.char}: {node.freq}')
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)

if __name__ == "__main__":
    chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    freqs = [19, 16, 17, 11, 42, 12, 14, 17, 16, 5, 10, 20, 19, 24, 18, 13, 1, 25, 35, 25, 15, 5, 21, 2, 8, 3]
    tree = HuffmanTree(chars, freqs)
    root = tree.huffman_tree()

    print('The tree in preorder is:')
    tree.preorder_traversal(root)



