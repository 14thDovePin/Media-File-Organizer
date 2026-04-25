def windows_file_namescheme(filename:str) -> str:
    """Filters a filename according to Window's filename scheme."""
    filename = filename.replace('<', '')
    filename = filename.replace('>', '')
    filename = filename.replace(':', '')
    filename = filename.replace('"', '')
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')
    filename = filename.replace('|', '')
    filename = filename.replace('?', '')
    filename = filename.replace('*', '')

    return filename