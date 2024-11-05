def get_file_extension(filename: str | None):
    if type(filename) == None:
        return None
    parts = filename.split('\.')
    if len(parts) < 2:
        return None
    elif len(parts) == 2:
        return parts[1]
    return parts[len(parts) - 1]