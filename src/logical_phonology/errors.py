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
    def __init__(self, s: str):
        self.value = s
        super().__init__(f"Invalid feature value '{s}'")


class UnknownFeatureError(ValidationError):
    def __init__(self, unknown: set[str]):
        self.unknown = unknown
        super().__init__(f"Unknown features '{unknown}'")


class ReservedFeatureError(ValidationError):
    def __init__(self, conflicts: frozenset[str]) -> None:
        self.conflicts = conflicts
        super().__init__(
            f"Feature names {conflicts} are reserved and cannot be used."
        )


class UnificationError(ValidationError):
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
    def __init__(self, features: frozenset[str]) -> None:
        self.features = features
        super().__init__(
            f"Features {features} are reserved and cannot be used in user-defined segments."  # noqa: E501
        )


class UnknownNameError(ValidationError):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(
            f"Unknown symbol name '{name}' not found in inventory."
        )


class UnknownSegmentError(ValidationError):
    def __init__(self, segment: Segment) -> None:
        self.segment = segment
        super().__init__(
            f"Unknown segment '{segment}' not found in inventory."
        )


class AliasError(ValidationError):
    def __init__(self, aliased: dict[str, list[str]]) -> None:
        self.aliased = aliased
        super().__init__(
            f"Aliases have been disabled. "
            f"The following segments have multiple names: {aliased}"
        )


class UntokenizableInputError(ValidationError):
    def __init__(self, input_str: str) -> None:
        self.input_str = input_str
        super().__init__(f"Could not tokenize input: '{input_str}'")


class AmbiguousTokenizationError(ValidationError):
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
    def __init__(self, conflicts: set[str]) -> None:
        self.conflicts = conflicts
        super().__init__(
            f"The following names already exist in the inventory: {conflicts}"
        )
