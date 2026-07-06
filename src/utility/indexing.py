def get_index_from_cardinal(cardinal: str) -> int:
    """Map an English cardinal label to a zero-based index."""
    index = -1
    match cardinal:
        case 'prima':
            index = 0
        case 'seconda':
            index = 1
        case 'terza':
            index = 2
        case 'quarta':
            index = 3
        case 'quinta':
            index = 4
    return index
