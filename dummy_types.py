from typing import Dict, Callable, Union

_RowType = Union[int, float, str]
CreatorType = Callable[..., _RowType]
RowDictType = Dict[str, _RowType]