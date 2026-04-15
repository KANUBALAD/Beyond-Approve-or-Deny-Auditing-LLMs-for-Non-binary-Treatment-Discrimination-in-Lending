
from __future__ import annotations
from pathlib import Path
import pandas as pd

from serializers import serialize_dataframe, save_serialized_outputs


# data_names = ["german", "hmda_ny", "hmda_tx", "homecredit"]
data_names = ["german", "hmda_ny", "hmda_tx"]
split_names = ["train", "test", "val"]


def run_one_job(input_csv: str, dataset_name: str, split_name: str, save_csv: bool = True) -> None:
    output_dir = Path("serialized_data")
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(input_csv)
    if not input_path.exists():
        print(f"Skipping missing file: {input_csv}")
        print("-" * 60)
        return

    base_name = f"{dataset_name}_{split_name}"
    output_json = output_dir / f"{base_name}.json"
    output_csv = output_dir / f"{base_name}.csv" if save_csv else None

    df = pd.read_csv(input_path)
    print(f"Loaded {input_csv} with shape {df.shape}")

    records = serialize_dataframe(df, dataset_name=dataset_name)
    save_serialized_outputs(
        records,
        str(output_json),
        str(output_csv) if output_csv else None,
    )

    print(f"Saved {len(records)} serialized rows to {output_json}")
    if output_csv:
        print(f"Saved tabular serialized view to {output_csv}")
    print("-" * 60)


def main():
    for dataset_name in data_names:
        for split_name in split_names:
            input_csv = f"./data/{dataset_name}_{split_name}.csv"
            run_one_job(
                input_csv=input_csv,
                dataset_name=dataset_name,
                split_name=split_name,
                save_csv=True,
            )


if __name__ == "__main__":
    main()