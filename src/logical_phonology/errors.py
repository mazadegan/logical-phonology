from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .feature_value import FeatureValue


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
