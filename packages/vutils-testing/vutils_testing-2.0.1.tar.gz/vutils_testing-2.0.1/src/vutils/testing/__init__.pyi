#
# File:    ./src/vutils/testing/__init__.pyi
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-17 14:14:50 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#

from collections.abc import Callable
from typing import Protocol
from unittest.mock import Mock, _patch

from typing_extensions import TypeAlias

ArgsType: TypeAlias = tuple[object, ...]
KwArgsType: TypeAlias = dict[str, object]
ExcType: TypeAlias = type[Exception]
MockableType: TypeAlias = Mock | object

ReturnsType: TypeAlias = object | Callable[[object], object] | None
SetupFuncType: TypeAlias = Callable[[MockableType], None] | None
BasesType: TypeAlias = type | tuple[type, ...] | None
MembersType: TypeAlias = KwArgsType | None
ExcSpecType: TypeAlias = ExcType | tuple[ExcType, ...]
PatchType: TypeAlias = _patch[MockableType]

class TypeType(Protocol):
    def __call__(self, *args: object, **kwargs: object) -> object: ...

class FuncType(Protocol):
    def __call__(self, *args: object, **kwargs: object) -> object: ...

def make_patch(
    target: object, mock: MockableType, **kwargs: object
) -> PatchType: ...
