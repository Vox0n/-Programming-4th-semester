def left_leaf(root):
    return root * 2


def right_leaf(root):
    return root + 3


def gen_bin_tree_iterative(root, height):
    tree = {}

    if height < 1:
        return tree

    queue = [(root, height)]

    while queue:
        current_root, current_height = queue.pop(0)

        if current_height > 0:
            tree[str(current_root)] = {}
            left = left_leaf(current_root)
            right = right_leaf(current_root)

            queue.append((left, current_height - 1))
            queue.append((right, current_height - 1))

    return tree
