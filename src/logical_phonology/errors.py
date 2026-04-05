class LogicalPhonologyError(Exception):
    """Base exception for all logical phonology errors."""

    pass


class ConfigError(LogicalPhonologyError):
    """Base exception for config errors."""

    pass


class MissingKeyError(ConfigError):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"Config missing '{key}' key.")


class InvalidTypeError(ConfigError):
    def __init__(self, key: str, expected: type) -> None:
        self.key = key
        self.expected = expected
        super().__init__(f"'{key}' must be a {expected.__name__}.")


class InvalidElementTypeError(ConfigError):
    def __init__(
        self, key: str, expected: type, invalid: list[object]
    ) -> None:
        self.key = key
        self.expected = expected
        self.invalid = invalid
        super().__init__(
            f"All elements of '{key}' must be {expected.__name__}. "
            f"Invalid values: {invalid}"
        )


class DuplicateFeaturesError(ConfigError):
    def __init__(self, duplicates: frozenset[str]) -> None:
        self.duplicates = duplicates
        super().__init__(
            f"All features must be unique. "
            f"Found multiple occurrences of: {duplicates}"
        )
