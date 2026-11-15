def is_hex_color(v):
    v = v.strip().lstrip('#')
    return len(v) in (3,6) and all(c in '0123456789abcdefABCDEF' for c in v)
