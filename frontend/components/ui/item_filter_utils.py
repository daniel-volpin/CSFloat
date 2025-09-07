from typing import List, Optional

WIDGET_KEY_PREFIX = "filters_"


def parse_csv_ints(raw: Optional[str]) -> Optional[List[int]]:
    """
    Parse a comma-separated string into a list of integers.

    Args:
        raw (Optional[str]): The raw input string to parse.

    Returns:
        Optional[List[int]]: List of integers if any found, else None.
    """
    if not raw:
        return None
    values = [x.strip() for x in str(raw).split(",")]
    ints = [int(x) for x in values if x.isdigit()]
    return ints or None
