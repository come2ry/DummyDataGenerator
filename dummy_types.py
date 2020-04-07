from typing import Dict, Callable, Union, List, Any
from datetime import date, datetime

_RowType = Union[int, float, str, 'date', Dict[str, Callable]]
CreatorType = Callable[...,  _RowType]
RowDictType = Dict[str, _RowType]