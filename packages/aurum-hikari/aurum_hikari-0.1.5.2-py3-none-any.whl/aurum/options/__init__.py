from __future__ import annotations

__all__: Sequence[str] = ("Choice", "Option")

import typing

from .choice import Choice
from .option import Option

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
