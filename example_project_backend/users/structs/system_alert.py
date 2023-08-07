from typing import TypedDict, Literal


class SystemAlert(TypedDict):
    name: str
    description: str
    level: Literal['error', 'warning']
