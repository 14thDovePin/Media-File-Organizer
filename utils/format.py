def se_number(num:int) -> str:
    """Formats an Episode or Season number to at least 2 digits."""
    string = str(num)

    if num < 10:
        return '0' + string
    else:
        return string