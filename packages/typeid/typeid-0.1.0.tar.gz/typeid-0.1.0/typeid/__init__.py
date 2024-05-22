""" UUID-compatible Typed IDs with prefixes.

    \b
        user_nnv5rr3rfk3hgry6xrygr
        └──┘ └───────────────────┘
        type    uuid (base58)

    First generate the Types using generate(...), then use them
    like so:

    >>> from uuid_extensions import uuid7
    >>> from typeid import generate
    >>> generate("sk", "pk", "user", "apikey")
    >>> assert str(SkId(uuid7().hex)).startswith("sk_")
    >>> assert str(PkId(uuid7().hex)).startswith("pk_")
    >>> assert str(UserId(uuid7().hex)).startswith("user_")
    >>> assert str(ApikeyId(uuid7().hex)).startswith("apikey_")
    >>> assert (UserId("user_nnv5rr3rfk3hgry6xrygr").hex 
    ...    == "0664c4135ed83faabd4bc0dc33839c9f")
    >>> generate("admin", suffix="IdUseWithCare")
    >>> assert str(AdminIdUseWithCare(uuid7().hex)).startswith("admin_")

    # Wrong prefix
    >>> UserId("sk_nnv5rr3rfk3hgry6xrygr")
    Traceback (most recent call last):
    ...
    ValueError: Wrong prefix, got sk, expected user

"""

from base58 import b58encode, b58decode
from uuid import UUID


class BaseId(UUID):
    """BaseID implementation that does the lifting of a UUID into a typed UUID
    and formats it more nicely.

    :param _prefix: The internal _prefix is filled in the generate() method
    """

    #: This class variable will be filled in by type() later own
    _prefix: str = ""

    def __init__(self, id: UUID | str | bytes):
        if isinstance(id, UUID):
            super().__init__(id.hex)
        elif isinstance(id, bytes):
            super().__init__(id.hex())
        elif isinstance(id, str):
            if id.startswith(self._prefix):
                prefix_free_id = id[len(self._prefix) + 1:]
                uid: bytes = b58decode(prefix_free_id)
                super().__init__(uid.hex())
            elif "_" in id:
                found_prefix = id[: id.index("_")]
                raise ValueError(
                    f"Wrong prefix, got {found_prefix}, expected {self._prefix}"
                )
            else:
                super().__init__(id)
        else:
            raise NotImplementedError(
                "Incorrect argument type. Requries, UUID, hex, bytes or string."
            )

    def __str__(self) -> str:
        """Prefix and base58 encode the id

        :return: encoded and prefixed id as string
        """
        prefix = str(self._prefix)
        id = b58encode(self.bytes).decode("ascii").lower()
        return f"{prefix}_{id}"


def generate(*args: str, suffix: str = "Id"):
    """Generate types based on a list of arguments. Each argument will result in
    a new type named after the argument (camel-cased) with the defined suffix at the end.
    """
    for _type in args:
        name = f"{_type.capitalize()}{suffix}"
        globals()[name] = type(name, (BaseId,), dict(_prefix=_type))


if __name__ == "__main__":
    import doctest

    generate("sk", "pk", "user", "apikey")
    generate("admin", suffix="IdUseWithCare")

    doctest.testmod()
