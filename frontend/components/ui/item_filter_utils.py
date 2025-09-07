from typing import List, Optional

WIDGET_KEY_PREFIX = "filters_"


def parse_csv_ints(raw: str | None) -> Optional[List[int]]:
    if not raw:
        return None
    values = [x.strip() for x in str(raw).split(",")]
    ints = [int(x) for x in values if x.isdigit()]
    return ints or None
