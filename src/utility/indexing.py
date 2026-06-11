def get_index_from_cardinal(cardinal: str) -> int:
    """Map an English cardinal label to a zero-based index."""
    index = -1
    match cardinal:
        case 'first':
            index = 0
        case 'second':
            index = 1
        case 'third':
            index = 2
        case 'fourth':
            index = 3
        case 'fifth':
            index = 4
    return index
