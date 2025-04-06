def print_preorder_traversal(self, node):
    """
    Prints the tree using preorder traversal as required by the lab.
    """
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
