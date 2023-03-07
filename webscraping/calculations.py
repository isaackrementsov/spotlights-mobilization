def subtree_moments(tree, root):
    size = 0
    sum_sizes = 0
    sum_sizes_sqrt = 0
    
    if len(tree[root].replies) == 0:
        size += 1
        sum_sizes += 1
        sum_sizes_sqr += 1
    else:
        for child in tree[root].replies:
            child_size, child_sum_size, child_sum_size_sqr = subtree_moments(tree, child)
            size += child_size
            sum_sizes += child_sum_size
            sum_sizes_sqr += child_sum_size_sqr

        size += 1
        sum_sizes += size
        sum_sizes_sqr += size ** 2
    
    return size, sum_sizes, sum_sizes_sqr

def virality(tree, root):
    size, sum_sizes, sum_sizes_sqr = subtree_moments(tree, root)
    return (2 * size / (size - 1)) * (sum_sizes / size - sum_sizes_sqr / size ** 2)