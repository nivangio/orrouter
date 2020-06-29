
def deduplicate_tuples_list_by_index_element(x,dedup_index):
    visited = set()

    # Output list initialization
    ret = []

    # Iteration
    for i in x:
        if not i[dedup_index] in visited:
            visited.add(i[dedup_index])
            ret.append(i)
    return ret