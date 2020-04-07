from typing import Dict, Callable, Union, List, Any
from datetime import date, datetime

RowType = Union[int, float, str, 'date', Dict[str, Any], List[Dict[str, Any]]]
CreatorType = Callable[...,  RowType]
RowDictType = Dict[str, RowType]