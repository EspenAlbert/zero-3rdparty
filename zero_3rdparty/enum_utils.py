from enum import Enum


class StrEnum(str, Enum):  # noqa: UP042 # uses a custom repr
    """Used to avoid the enum repr: "<_Status.STARTED: 'STARTED'>"."""

    def __repr__(self) -> str:
        return str.__repr__(self)

    def __str__(self) -> str:
        return str.__str__(self)
