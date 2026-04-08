from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .feature_value import FeatureValue
    from .segment import Segment
    from .word import Word


class LogicalPhonologyError(Exception):
    """Base exception for all logical phonology errors."""

    pass


class ValidationError(LogicalPhonologyError):
    """Base exception for validation errors."""

    pass


class InvalidFeatureValueError(ValidationError):
    """Raised when a string cannot be parsed as a FeatureValue.

    Attributes:
        value: The invalid string that was passed to `FeatureValue.from_str`.
    """

    def __init__(self, s: str):
        self.value = s
        super().__init__(f"Invalid feature value '{s}'")


class UnknownFeatureError(ValidationError):
    """Raised when a feature name is not in the valid feature set.

    Attributes:
        unknown: The set of unrecognized feature names.
    """

    def __init__(self, unknown: set[str]):
        self.unknown = unknown
        super().__init__(f"Unknown features '{unknown}'")


class ReservedFeatureError(ValidationError):
    """Raised when a FeatureSystem is initialized with reserved feature names.

    Reserved feature names (e.g. 'BOS', 'EOS') are used internally by the
    library and cannot be used in user-defined feature systems.

    Attributes:
        conflicts: The set of reserved feature names that were used.
    """

    def __init__(self, conflicts: frozenset[str]) -> None:
        self.conflicts = conflicts
        super().__init__(
            f"Feature names {conflicts} are reserved and cannot be used."
        )


class UnificationError(ValidationError):
    """Raised by `Segment.unify_strict` when two segments have conflicting
    values for the same feature.

    Attributes:
        feature: The feature name on which unification failed.
        v1: The value of the feature in the first segment.
        v2: The conflicting value of the feature in the second segment.
    """

    def __init__(
        self, feature: str, v1: FeatureValue, v2: FeatureValue
    ) -> None:
        self.feature = feature
        self.v1 = v1
        self.v2 = v2
        super().__init__(
            f"Unification failed on feature '{feature}': {v1} conflicts with {v2}."  # noqa: E501
        )


class ReservedFeatureUsageError(ValidationError):
    """Raised when a user attempts to construct a segment using reserved
    feature names such as 'BOS' or 'EOS'.

    Attributes:
        features: The set of reserved feature names that were used.
    """

    def __init__(self, features: frozenset[str]) -> None:
        self.features = features
        super().__init__(
            f"Features {features} are reserved and cannot be used in user-defined segments."  # noqa: E501
        )


class UnknownNameError(ValidationError):
    """Raised when a name is not found in an inventory.

    Attributes:
        name: The name that was not found.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(
            f"Unknown symbol name '{name}' not found in inventory."
        )


class UnknownSegmentError(ValidationError):
    """Raised when a segment is not found in an inventory.

    Attributes:
        segment: The segment that was not found.
    """

    def __init__(self, segment: Segment) -> None:
        self.segment = segment
        super().__init__(
            f"Unknown segment '{segment}' not found in inventory."
        )


class AliasError(ValidationError):
    """Raised when aliases are detected in an inventory where
    `allow_aliases=False`.

    Attributes:
        aliased: A dict mapping canonical segment forms to the list of
            names that refer to them.
    """

    def __init__(self, aliased: dict[str, list[str]]) -> None:
        self.aliased = aliased
        super().__init__(
            f"Aliases have been disabled. "
            f"The following segments have multiple names: {aliased}"
        )


class UntokenizableInputError(ValidationError):
    """Raised when a string cannot be tokenized using the inventory.

    Attributes:
        input_str: The input string that could not be tokenized.
    """

    def __init__(self, input_str: str) -> None:
        self.input_str = input_str
        super().__init__(f"Could not tokenize input: '{input_str}'")


class AmbiguousTokenizationError(ValidationError):
    """Raised when a string has multiple valid tokenizations and
    `allow_ambiguity=False`.

    Attributes:
        input_str: The input string that was ambiguously tokenized.
        tokenizations: All possible tokenizations as a list of Words.
    """

    def __init__(self, input_str: str, tokenizations: list[Word]) -> None:
        self.input_str = input_str
        self.tokenizations = tokenizations
        rendered = [" ".join(str(s) for s in w) for w in tokenizations]
        super().__init__(
            f"Ambiguous tokenization for input: '{input_str}'. "
            f"Found {len(tokenizations)} possible parses:\n"
            + "\n".join(rendered)
        )


class DuplicateNameError(ValidationError):
    """Raised when attempting to add a name to an inventory that already
    exists.

    Attributes:
        conflicts: The set of names that already exist in the inventory.
    """

    def __init__(self, conflicts: set[str]) -> None:
        self.conflicts = conflicts
        super().__init__(
            f"The following names already exist in the inventory: {conflicts}"
        )
