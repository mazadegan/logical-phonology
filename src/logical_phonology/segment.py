from dataclasses import dataclass

from .feature_value import FeatureValue


@dataclass(frozen=True)
class Segment:
    features: dict[str, FeatureValue]

    # dict are not hashable, must use frozenset of features' items
    def __hash__(self) -> int:
        return hash((frozenset(self.features.items())))

    def __getitem__(self, key: str) -> FeatureValue:
        return self.features[key]

    def __contains__(self, item: str) -> bool:
        return item in self.features
