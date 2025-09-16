class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0

def height(node):
    return -1 if node is None else node.height

def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))

def balance_factor(node):
    return height(node.left) - height(node.right)

def rotate_right(z):
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3
    update_height(z)
    update_height(y)
    return y

def rotate_left(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    update_height(z)
    update_height(y)
    return y

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

def min_value_node(n):
    cur = n
    while cur.left is not None:
        cur = cur.left
    return cur

def delete(node, key):
    if node is None:
        return node, False
    if key < node.key:
        node.left, removed = delete(node.left, key)
    elif key > node.key:
        node.right, removed = delete(node.right, key)
    else:
        if node.left is None and node.right is None:
            return None, True
        elif node.left is None:
            return node.right, True
        elif node.right is None:
            return node.left, True
        else:
            succ = min_value_node(node.right)
            node.key = succ.key
            node.right, removed = delete(node.right, succ.key)
    if not removed:
        return node, False
    update_height(node)
    node = rebalance(node)
    return node, True

def preorder(n, out):
    if n is None:
        return
    out.append(str(n.key))
    preorder(n.left, out)
    preorder(n.right, out)

def inorder(n, out):
    if n is None:
        return
    inorder(n.left, out)
    out.append(str(n.key))
    inorder(n.right, out)

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
