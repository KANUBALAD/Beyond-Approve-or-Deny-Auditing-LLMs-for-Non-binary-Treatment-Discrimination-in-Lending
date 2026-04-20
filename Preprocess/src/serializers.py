from __future__ import annotations
import json as json_lib
from typing import Any, Dict, List
import pandas as pd

from dataset_configs import (
    DATASET_CONFIGS,
    decode_value,
    pythonize_number,
)


SERIALIZATION_COLUMNS = ["great", "text", "html", "json"]


def normalize_column_name(col: str) -> str:
    if col.endswith("_F"):
        return col[:-2]
    elif col.endswith("_CF"):
        return col[:-3]
    elif col.endswith("_cf"):
        return col[:-3]
    return col


def normalize_row(
    row: Dict[str, Any],
    drop_columns: List[str] | None = None,
) -> Dict[str, Any]:
    drop_columns = drop_columns or []
    normalized: Dict[str, Any] = {}
    for col, value in row.items():
        if col in drop_columns:
            continue
        base_col = normalize_column_name(col)
        normalized[base_col] = pythonize_number(value)
    return normalized


def decode_section(section: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        feature: decode_value(feature, value, config)
        for feature, value in section.items()
    }


def build_record(row: Dict[str, Any], dataset_name: str, row_id: int | None = None) -> Dict[str, Any]:
    config = DATASET_CONFIGS[dataset_name]
    normalized_row = normalize_row(
        row=row,
        drop_columns=config.get("drop_from_main_json", []),
    )
    decoded_row = decode_section(normalized_row, config)
    return {
        "row_id": row_id,
        "raw": normalized_row,
        "decoded": decoded_row,
    }


def flatten_record_columns(record: Dict[str, Any]) -> Dict[str, Any]:
    return dict(record["decoded"])


def render_json(record: Dict[str, Any]) -> str:
    return json_lib.dumps(record["decoded"], ensure_ascii=False)


def render_great(flat_row: Dict[str, Any]) -> str:
    return ", ".join([f"{k} is {v}" for k, v in flat_row.items()])


def render_list(flat_row: Dict[str, Any]) -> str:
    return "\n".join([f"- {k} : {v}" for k, v in flat_row.items()])


def render_text(flat_row: Dict[str, Any]) -> str:
    return " ".join([f"The {k} is {v}." for k, v in flat_row.items()])


# def render_html(flat_row: Dict[str, Any]) -> str:
#     df = pd.DataFrame([flat_row])
#     return df.to_html(index=False)

def render_html(flat_row: Dict[str, Any]) -> str:
    headers = "".join(f"<th>{k}</th>" for k in flat_row.keys())
    values = "".join(f"<td>{v}</td>" for v in flat_row.values())
    return f"<table><thead><tr>{headers}</tr></thead><tbody><tr>{values}</tr></tbody></table>"

def serialize_record(record: Dict[str, Any], dataset_name: str) -> Dict[str, Any]:
    flat_row = flatten_record_columns(record)

    output = dict(flat_row)
    output["great"] = render_great(flat_row)
    # output["list"] = render_list(flat_row)
    output["text"] = render_text(flat_row)
    output["html"] = render_html(flat_row)
    output["json"] = render_json(record)

    return output


# def serialize_dataframe(df: pd.DataFrame, dataset_name: str) -> List[Dict[str, Any]]:
#     records = []
#     for idx, row in df.iterrows():
#         row_dict = row.to_dict()
#         record = build_record(row=row_dict, dataset_name=dataset_name, row_id=idx)
#         serialized = serialize_record(record, dataset_name)
#         records.append(serialized)
#     return records

def serialize_dataframe(df: pd.DataFrame, dataset_name: str) -> List[Dict[str, Any]]:
    records = []
    for idx, row_dict in enumerate(df.to_dict(orient="records")):
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
        json_lib.dump(records, f, indent=2, ensure_ascii=False)

    if output_csv_path is not None:
        pd.DataFrame(records).to_csv(output_csv_path, index=False)