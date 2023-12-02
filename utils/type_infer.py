def convert_to_proper_type(value):
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value