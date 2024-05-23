"""
This python module contains useful methods
"""

from __future__ import annotations
from typing import Any
from typing import Union
from datetime import datetime
from pytz import timezone
from urllib.parse import urlparse


Numbers = Union[float, int]


def get_utc_timestamp() -> float:
    """DOCSTRING"""
    return datetime.now(timezone("UTC")).timestamp()


def get_utc_timestr(format: str = "%d/%b/%Y %H.%M.%S") -> str:
    return datetime.now(timezone("UTC")).strftime(format)


def print_exception(e: Union[Exception, str]) -> None:
    """DOCTSTRING"""
    
    if isinstance(e, Exception):
        e = str(e)

    timestr = get_utc_timestr()
    print(f"127.0.0.1 - - [{timestr}] ERROR: {e.capitalize()}")


def get_value_in_dict(map: dict, key: Any) -> Any:
    """
    Return the value of a key in a dictionary.
    In the key is not found, return None.
    """

    if key in map:
        return map[key]
    else:
        return None


def get_absolute_path(origin: str, relative_path: str) -> str:
    """DOCSTRING"""
    org_parsed = urlparse(origin)
    rel_parsed = urlparse(relative_path)
    if rel_parsed.scheme == "http" or rel_parsed.scheme == "https":
        return relative_path
    elif relative_path.startswith("//"):
        return f"{org_parsed.scheme}:{relative_path}"
    elif relative_path.startswith("/"):
        origin_host = org_parsed.hostname
        if org_parsed.port is not None:
            origin_host += f":{org_parsed.port}"
        return f"{org_parsed.scheme}://{origin_host}{relative_path}"
    else:
        origin_host = org_parsed.hostname
        if org_parsed.port is not None:
            origin_host += f":{org_parsed.port}"

        origin_path = org_parsed.path
        if not origin_path.endswith("/"):
            origin_path_obj = origin_path.split("/")
            origin_path_obj.pop()
            origin_path = "/" + "/".join(origin_path_obj) + "/"

        return f"{org_parsed.scheme}://{origin_host}{origin_path}{relative_path}"
