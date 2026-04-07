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
