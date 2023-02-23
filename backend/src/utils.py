from typing import List, Dict
import dataclasses
from fastapi import HTTPException


def str_to_list(string: str) -> list:
    """Convert a comma-separated string to a list"""
    return string.split(",")


def format_query_result(result_list: List) -> List[Dict]:
    """Convert a list of objects to a list of dicts"""
    return [dataclasses.asdict(element) for element in result_list]


def http_exception():
    """Return a 404 HTTPException"""
    return HTTPException(status_code=404, detail=" ID Not Found ")