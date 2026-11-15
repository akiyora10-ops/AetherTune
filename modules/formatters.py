def bytes_to_mb(b):
    return round(b/1048576, 2)

def percent_bar(p):
    return '[' + '#' * (p//10) + '-' * (10 - p//10) + ']'
