# pointer-based node with cached height
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0

# height with the empty subtree defined as -1 so a leaf has height 0
def height(node):
    return -1 if node is None else node.height

# height update after structural change: 1 + max(height(left), height(right))
def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))

# balance factor: height(left) minus height(right); AVL keeps this difference no more than 1
def balance_factor(node):
    return height(node.left) - height(node.right)

# right rotation around z; updates height
def rotate_right(z):
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3
    update_height(z)
    update_height(y)
    return y

# left rotation around z; updates height
def rotate_left(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    update_height(z)
    update_height(y)
    return y

# rebalance by applying the appropriate rotation based on the balance factor
def rebalance(n):
    bf = balance_factor(n)
    if bf > 1:
        if balance_factor(n.left) < 0:
            n.left = rotate_left(n.left)
        return rotate_right(n)
    if bf < -1:
        if balance_factor(n.right) > 0:
            n.right = rotate_right(n.right)
        return rotate_left(n)
    return n

# insert key if absent; returns (new_root, changed_flag)
def insert(node, key):
    if node is None:
        return Node(key), True
    if key == node.key:
        return node, False
    if key < node.key:
        node.left, changed = insert(node.left, key)
    else:
        node.right, changed = insert(node.right, key)
    if changed:
        update_height(node)
        node = rebalance(node)
    return node, changed

# predecessor helper: largest key in the left subtree
def max_value_node(n: Node) -> Node:
    cur = n
    while cur.right is not None:
        cur = cur.right
    return cur

# delete key if present; returns (new_root, removed_flag)
def delete(node: "Node | None", key: int) -> tuple["Node | None", bool]:
    if node is None:
        return node, False
    if key < node.key:
        node.left, removed = delete(node.left, key)
    elif key > node.key:
        node.right, removed = delete(node.right, key)
    else:
        if node.left is None and node.right is None:
            return None, True
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        pred = max_value_node(node.left)
        node.key = pred.key
        node.left, removed = delete(node.left, pred.key)
    if not removed:
        return node, False
    update_height(node)
    node = rebalance(node)
    return node, True

# preorder traversal into a list of strings
def preorder(n, out):
    if n is None:
        return
    out.append(str(n.key))
    preorder(n.left, out)
    preorder(n.right, out)

# inorder traversal into a list of strings
def inorder(n, out):
    if n is None:
        return
    inorder(n.left, out)
    out.append(str(n.key))
    inorder(n.right, out)

# postorder traversal into a list of strings
def postorder(n, out):
    if n is None:
        return
    postorder(n.left, out)
    postorder(n.right, out)
    out.append(str(n.key))

def main():
    data = input().split()
    if not data:
        print("EMPTY")
        return
    root = None
    finish = data[-1]
    for tok in data[:-1]:
        op = tok[0]
        val = int(tok[1:])
        if op == 'A':
            root, _ = insert(root, val)
        elif op == 'D':
            root, _ = delete(root, val)
    if root is None:
        print("EMPTY")
        return
    out = []
    if finish == 'PRE':
        preorder(root, out)
    elif finish == 'IN':
        inorder(root, out)
    elif finish == 'POST':
        postorder(root, out)
    else:
        inorder(root, out)
    print(' '.join(out))

if __name__ == "__main__":
    main()
