from enum import Enum

from .errors import InvalidFeatureValueError


class FeatureValue(Enum):
    """A binary feature value in Logical Phonology.

    A segment may also be underspecified for a feature, in which case
    that feature is simply absent from the segment's feature bundle.

    Attributes:
        POS: Positive feature value, represented as `+`.
        NEG: Negative feature value, represented as `-`.
    """

    POS = "+"
    NEG = "-"

    def __str__(self) -> str:
        """Return the string representation of the feature value."""
        return self.value

    @classmethod
    def from_str(cls, input_string: str) -> "FeatureValue":
        """Parse a string into a FeatureValue.

        Args:
            input_string: A string representation of a feature value. Must be
                `'+'` or `'-'`.

        Returns:
            The corresponding FeatureValue.

        Raises:
            InvalidFeatureValueError: If the string is not a valid
                feature value.
        """
        for member in cls:
            if member.value == input_string:
                return member
        raise InvalidFeatureValueError(input_string)


POS = FeatureValue.POS
"""Alias for `FeatureValue.POS`."""

NEG = FeatureValue.NEG
"""Alias for `FeatureValue.NEG`."""
