from __future__ import annotations
import json
import html
from typing import Any, Dict, List, Tuple

import pandas as pd

from dataset_configs import (
    DATASET_CONFIGS,
    decode_value,
    display_name,
    # derived_display_name,
    path_sensitive_cf_display_name,
    pythonize_number,
)


def split_factual_counterfactual(
    row: Dict[str, Any],
    factual_suffix: str = "_F",
    counterfactual_suffix: str = "_CF",
    drop_columns: List[str] | None = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Split a flat row into factual, counterfactual, and path_sensitive_cf buckets.
    """
    drop_columns = drop_columns or []

    factual: Dict[str, Any] = {}
    counterfactual: Dict[str, Any] = {}
    path_sensitive_cf: Dict[str, Any] = {}

    for col, value in row.items():
        if col in drop_columns:
            continue

        value = pythonize_number(value)

        if col.endswith(factual_suffix):
            base = col[: -len(factual_suffix)]
            factual[base] = value
        elif col.endswith(counterfactual_suffix):
            base = col[: -len(counterfactual_suffix)]
            counterfactual[base] = value
        else:
            path_sensitive_cf[col] = value

    return {
        "factual": factual,
        "counterfactual": counterfactual,
        "path_sensitive_cf": path_sensitive_cf,
    }


def decode_section(section: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    decoded = {}
    for feature, value in section.items():
        decoded[feature] = decode_value(feature, value, config)
    return decoded


def build_record(row: Dict[str, Any], dataset_name: str, row_id: int | None = None) -> Dict[str, Any]:
    config = DATASET_CONFIGS[dataset_name]

    record = split_factual_counterfactual(
        row=row,
        factual_suffix=config["factual_suffix"],
        counterfactual_suffix=config["counterfactual_suffix"],
        drop_columns=config.get("drop_from_main_json", []),
    )

    factual_decoded = decode_section(record["factual"], config)
    counterfactual_decoded = decode_section(record["counterfactual"], config)

    path_sensitive_cf_decoded = {}
    for k, v in record["path_sensitive_cf"].items():
        if k.startswith("class_"):
            path_sensitive_cf_decoded[k] = decode_value("class", v, config)
        else:
            path_sensitive_cf_decoded[k] = pythonize_number(v)

    return {
        "row_id": row_id,
        "factual": record["factual"],
        "counterfactual": record["counterfactual"],
        "path_sensitive_cf": record["path_sensitive_cf"],
        "decoded_factual": factual_decoded,
        "decoded_counterfactual": counterfactual_decoded,
        "decoded_path_sensitive_cf": path_sensitive_cf_decoded,
    }


def changed_and_unchanged_features(
    factual: Dict[str, Any],
    counterfactual: Dict[str, Any],
) -> Tuple[List[str], List[str]]:
    shared = sorted(set(factual) & set(counterfactual))
    changed = []
    unchanged = []

    for feature in shared:
        if factual[feature] != counterfactual[feature]:
            changed.append(feature)
        else:
            unchanged.append(feature)

    return changed, unchanged


def render_json(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "row_id": record["row_id"],
        "factual": record["decoded_factual"],
        "counterfactual": record["decoded_counterfactual"],
        "path_sensitive_cf": record["decoded_path_sensitive_cf"],
    }


def render_great(record: Dict[str, Any], config: Dict[str, Any]) -> str:
    pieces = []

    for feature, value in record["decoded_factual"].items():
        pieces.append(f"factual {display_name(feature, config)} is {value}")

    for feature, value in record["decoded_counterfactual"].items():
        pieces.append(f"counterfactual {display_name(feature, config)} is {value}")

    for feature, value in record["decoded_path_sensitive_cf"].items():
        pieces.append(f"{path_sensitive_cf_display_name(feature, config)} is {value}")

    return ", ".join(pieces)


def render_text(record: Dict[str, Any], config: Dict[str, Any]) -> str:
    sentences = []

    for feature, value in record["decoded_factual"].items():
        sentences.append(f"The factual {display_name(feature, config)} is {value}.")

    for feature, value in record["decoded_counterfactual"].items():
        sentences.append(f"The counterfactual {display_name(feature, config)} is {value}.")

    for feature, value in record["decoded_path_sensitive_cf"].items():
        sentences.append(f"The {path_sensitive_cf_display_name(feature, config)} is {value}.")

    return " ".join(sentences)


def render_html(record: Dict[str, Any], config: Dict[str, Any]) -> str:
    factual = record["decoded_factual"]
    counterfactual = record["decoded_counterfactual"]
    path_sensitive_cf = record["decoded_path_sensitive_cf"]

    all_features = sorted(set(factual) | set(counterfactual))
    changed, unchanged = changed_and_unchanged_features(factual, counterfactual)

    rows = []
    for feature in all_features:
        label = html.escape(display_name(feature, config))
        f_val = html.escape(str(factual.get(feature, "")))
        cf_val = html.escape(str(counterfactual.get(feature, "")))
        status = "changed" if feature in changed else "unchanged"
        rows.append(
            f"<tr><td>{label}</td><td>{f_val}</td><td>{cf_val}</td><td>{status}</td></tr>"
        )

    path_sensitive_cf_items = []
    for feature, value in path_sensitive_cf.items():
        label = html.escape(path_sensitive_cf_display_name(feature, config))
        val = html.escape(str(value))
        path_sensitive_cf_items.append(f"<li><strong>{label}:</strong> {val}</li>")

    row_id = "" if record["row_id"] is None else str(record["row_id"])

    html_text = f"""
<div class="record">
  <h2>Record {html.escape(row_id)}</h2>

  <h3>Factual vs Counterfactual</h3>
  <table border="1" cellpadding="6" cellspacing="0">
    <thead>
      <tr>
        <th>Feature</th>
        <th>Factual</th>
        <th>Counterfactual</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>

  <h3>Path Sensitive Counterfactuals</h3>
  <ul>
    {''.join(path_sensitive_cf_items)}
  </ul>
</div>
""".strip()

    return html_text


def render_lift(record: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Generic LIFT-style narrative for factual/counterfactual records.
    This is domain-aware but not brittle.
    """
    factual = record["decoded_factual"]
    counterfactual = record["decoded_counterfactual"]
    derived = record["decoded_path_sensitive_cf"]

    changed, unchanged = changed_and_unchanged_features(factual, counterfactual)

    age_f = factual.get("age", "unknown")
    gender_f = factual.get("gender", "unknown")
    duration_f = factual.get("duration", "unknown")
    credit_amount_f = factual.get("credit_amount", "unknown")
    purpose_f = factual.get("purpose", "unknown")
    class_f = factual.get("class", "unknown")

    age_cf = counterfactual.get("age", "unknown")
    gender_cf = counterfactual.get("gender", "unknown")
    duration_cf = counterfactual.get("duration", "unknown")
    credit_amount_cf = counterfactual.get("credit_amount", "unknown")
    purpose_cf = counterfactual.get("purpose", "unknown")
    class_cf = counterfactual.get("class", "unknown")

    changed_bits = []
    for feature in changed:
        if feature == "class":
            continue
        changed_bits.append(
            f"{display_name(feature, config)} changes from {factual[feature]} to {counterfactual[feature]}"
        )

    unchanged_bits = []
    for feature in unchanged:
        if feature in {"age", "gender", "duration", "credit_amount", "purpose", "class"}:
            continue
        unchanged_bits.append(
            f"{display_name(feature, config)} remains {factual[feature]}"
        )

    derived_sentence = []
    for key, value in derived.items():
        derived_sentence.append(f"{path_sensitive_cf_display_name(key, config)} is {value}")

    changed_text = "; ".join(changed_bits) if changed_bits else "no features change"
    unchanged_text = "; ".join(unchanged_bits[:5]) if unchanged_bits else ""
    derived_text = "; ".join(derived_sentence)

    narrative = (
        f"The factual applicant is a {age_f}-year-old {gender_f} requesting a credit amount of "
        f"{credit_amount_f} for {duration_f} months for {purpose_f}. "
        f"The factual class is {class_f}. "
        f"The counterfactual applicant is a {age_cf}-year-old {gender_cf} requesting a credit amount of "
        f"{credit_amount_cf} for {duration_cf} months for {purpose_cf}. "
        f"The counterfactual class is {class_cf}. "
        f"Relative to the factual instance, {changed_text}. "
    )

    if unchanged_text:
        narrative += f"Some other attributes stay fixed: {unchanged_text}. "

    if derived_text:
        narrative += f"Derived outputs are as follows: {derived_text}."

    return narrative.strip()


def serialize_record(record: Dict[str, Any], dataset_name: str) -> Dict[str, Any]:
    config = DATASET_CONFIGS[dataset_name]

    return {
        "row_id": record["row_id"],
        "json": render_json(record),
        "text": render_text(record, config),
        "great": render_great(record, config),
        # "html": render_html(record, config),
        "LIFT": render_lift(record, config),
    }


def serialize_dataframe(df: pd.DataFrame, dataset_name: str) -> List[Dict[str, Any]]:
    records = []
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        record = build_record(row=row_dict, dataset_name=dataset_name, row_id=idx)
        serialized = serialize_record(record, dataset_name)
        records.append(serialized)
    return records


def save_serialized_outputs(
    records: List[Dict[str, Any]],
    output_json_path: str,
    output_csv_path: str | None = None,
) -> None:
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    if output_csv_path is not None:
        pd.DataFrame(records).to_csv(output_csv_path, index=False)