def convert_floats_to_strings(d):
    """Convert floats in a dictionary to strings.

    Args:
        d (dict): The dictionary to convert.

    Returns:
        dict: The dictionary with floats converted to strings.
    """
    if not isinstance(d, dict):
        return d

    converted_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            converted_dict[key] = convert_floats_to_strings(value)
        elif isinstance(value, float):
            converted_dict[key] = str(value)
        else:
            converted_dict[key] = value

    return converted_dict