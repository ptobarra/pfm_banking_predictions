separator = '='

# Gets the properties of the provided file.
def load_properties(filepath):
    """
    Read the file passed as parameter as a properties file.
    """
    comment_char = '#'
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(separator)
                key = key_value[0].strip()
                value = separator.join(key_value[1:]).strip().strip('"') 
                props[key] = value 
    return props