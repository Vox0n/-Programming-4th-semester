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


if __name__ == '__main__':
    root_value = 2
    height_value = 3

    print("Рекурсивное построение дерева:")
    recursive_tree = gen_bin_tree_recursive(root_value, height_value)
    print(recursive_tree)

    print("\nНерекурсивное построение дерева:")
    iterative_tree = gen_bin_tree_iterative(root_value, height_value)
    print(iterative_tree)

