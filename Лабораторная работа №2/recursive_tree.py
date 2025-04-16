def left_leaf(root):
    return root * 2


def right_leaf(root):
    return root + 3


def gen_bin_tree_recursive(root, height):
    if height == 0:
        return {}
    return {
        str(root): [
            gen_bin_tree_recursive(left_leaf(root), height - 1),
            gen_bin_tree_recursive(right_leaf(root), height - 1)
        ]
    }
