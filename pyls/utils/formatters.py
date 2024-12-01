"""Module providing various formatter."""

from math import ceil


def humanize_size(size: float) -> str:
    """Convert a file size in bytes to a human-readable
    string with appropriate units.

    Parameters
    ----------
    size : float
        The size in bytes to be converted.

    Returns
    ----------
    humanized_size : str
        A human-readable size string with a unit suffix (e.g., "1.5K", "2M").
    """
    if size == 0:
        return "0"
    units = ["", "K", "M", "G", "T", "P", "E"]
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    size = ceil(size * 10) / 10 if size < 10 else ceil(size)
    if size >= 10:
        return f"{size:.0f}{units[unit_index]}"
    else:
        return f"{size:.1f}{units[unit_index]}"
