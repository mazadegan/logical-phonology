__version__ = "0.1.0"

from .errors import (
    ConfigError,
    DuplicateFeaturesError,
    InvalidElementTypeError,
    InvalidTypeError,
    LogicalPhonologyError,
    MissingKeyError,
)
from .feature_matrix import load_feature_system

__all__ = [
    "__version__",
    "ConfigError",
    "DuplicateFeaturesError",
    "InvalidElementTypeError",
    "InvalidTypeError",
    "LogicalPhonologyError",
    "MissingKeyError",
    "load_feature_system",
]
