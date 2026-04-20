from pathlib import Path
import pandas as pd

from serializers import serialize_dataframe, save_serialized_outputs

data_names = ["german", "hmda_ny", "hmda_tx", "homecredit"]

def infer_file_info(filename: str):
    name = filename.replace(".csv", "")
    if "_factual_" in name:
        data_kind = "factual"
        split = name.split("_factual_")[-1]
    elif "_cf_" in name:
        data_kind = "pathspecific"
        remainder = name.split("_cf_")[-1]
        split = remainder.split("_")[0]   # test from test_gender, val from val_gender
    else:
        return None, None
    return data_kind, split

def run_one_job(input_csv: Path, dataset_name: str, data_kind: str, split_name: str):
    output_dir = Path("serialized_datasets") / dataset_name / data_kind
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir / f"{split_name}.json"
    df = pd.read_csv(input_csv)
    # print(f"Loaded {input_csv} with shape {df.shape}")
    records = serialize_dataframe(df, dataset_name=dataset_name)
    save_serialized_outputs(records, str(output_json))
    # print(f"Saved to {output_json}")


def main():
    preprocessed_root = Path("../preprocessed_data")
    for dataset_name in data_names:
        dataset_dir = preprocessed_root / dataset_name
        if not dataset_dir.exists():
            print(f"Missing folder: {dataset_dir}")
            continue
        for csv_file in dataset_dir.glob("*.csv"):
            data_kind, split_name = infer_file_info(csv_file.name)
            run_one_job(
                input_csv=csv_file,
                dataset_name=dataset_name,
                data_kind=data_kind,
                split_name=split_name,
            )

if __name__ == "__main__":
    main()




