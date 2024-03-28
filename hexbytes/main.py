from typing import (
    TYPE_CHECKING,
    Type,
    Union,
    cast,
    overload,
)

from ._utils import (
    to_bytes,
)

if TYPE_CHECKING:
    from typing import (
        SupportsIndex,
    )

BytesLike = Union[bool, bytearray, bytes, int, str, memoryview]


class HexBytes(bytes):
    """
    HexBytes is a *very* thin wrapper around the python built-in :class:`bytes` class.

    It has these changes:
        1. Accepts more initializing values, like hex strings, non-negative integers,
           and booleans
        2. The representation at console (__repr__) is 0x-prefixed
        3. The to_0x_hex method is added to convert the bytes to a 0x-prefixed hex string
    """  # noqa: E501

    def __new__(cls: Type[bytes], val: BytesLike) -> "HexBytes":
        bytesval = to_bytes(val)
        return cast(HexBytes, super().__new__(cls, bytesval))  # type: ignore  # https://github.com/python/typeshed/issues/2630  # noqa: E501

    @overload
    def __getitem__(self, key: "SupportsIndex") -> int:  # noqa: F811
        ...

    @overload  # noqa: F811
    def __getitem__(self, key: slice) -> "HexBytes":  # noqa: F811
        ...

    def __getitem__(  # noqa: F811
        self, key: Union["SupportsIndex", slice]
    ) -> Union[int, bytes, "HexBytes"]:
        result = super().__getitem__(key)
        if hasattr(result, "hex"):
            return type(self)(result)
        else:
            return result

    def __repr__(self) -> str:
        return f"HexBytes({self.to_0x_hex()!r})"

    def to_0x_hex(self) -> str:
        """
        Convert the bytes to a 0x-prefixed hex string
        """
        return f"0x{self.hex()}"
