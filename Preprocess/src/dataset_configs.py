from __future__ import annotations

from typing import Any, Dict

from german_config import GERMAN_CONFIG
from hmda_config import HMDA_CONFIG
from homecredit_config import HOMECREDIT_CONFIG


DATASET_CONFIGS = {
    "german": GERMAN_CONFIG,
    "hmda_ny": HMDA_CONFIG,
    "hmda_tx": HMDA_CONFIG,
    "homecredit": HOMECREDIT_CONFIG,
}

def pythonize_number(x: Any) -> Any:
    """Convert numpy-ish scalars to regular Python values where possible."""
    try:
        if x is None:
            return None
        if hasattr(x, "item"):
            x = x.item()
        if isinstance(x, float) and x.is_integer():
            return int(x)
        return x
    except Exception:
        return x


def decode_value(feature: str, value: Any, config: Dict[str, Any]) -> Any:
    """Decode coded categorical values using config mappings, otherwise return raw."""
    value = pythonize_number(value)
    value_maps = config.get("value_maps", {})
    feature_map = value_maps.get(feature)
    if feature_map is None:
        return value
    if value in feature_map:
        return feature_map[value]
    return value


def display_name(feature: str, config: Dict[str, Any]) -> str:
    """Human-readable label for a feature."""
    return config.get("feature_labels", {}).get(
        feature,
        feature.replace("_", " ")
    )


def path_sensitive_cf_display_name(feature: str, config: Dict[str, Any]) -> str:
    return config.get("path_sensitive_cf_labels", {}).get(
        feature,
        feature.replace("_", " ")
    )
    
    