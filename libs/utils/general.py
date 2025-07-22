import re
from typing import Tuple


def split_name(full_name: str) -> Tuple[str, str]:
    """Split full name to first name and the rest.

    We can't figure out if there are more first names or last names
    """
    first_name, *rest_names = re.split(r"\s+", full_name.strip())
    return first_name, " ".join(rest_names)
