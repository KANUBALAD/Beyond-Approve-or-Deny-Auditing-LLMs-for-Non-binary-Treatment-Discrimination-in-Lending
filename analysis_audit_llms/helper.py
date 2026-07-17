
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer


def build_factual_truth_lookup(factual_jsonl_file):
    truth_lookup = {}
    with open(factual_jsonl_file, "r") as f:
        for line in f:
            ex = json.loads(line)
            doc_id = ex.get("doc_id")
            doc = ex.get("doc", {})
            truth_lookup[doc_id] = {
                "true_amount": doc.get("credit_amount"),
                "true_duration": doc.get("duration"),
            }

    return truth_lookup

def extract_prediction_and_justification(text):
    amount_match = re.search(r"Loan Amount:\s*([0-9]+)", text)
    duration_match = re.search(r"Loan Duration:\s*([0-9]+)", text)
    pred_amount = int(amount_match.group(1)) if amount_match else None
    pred_duration = int(duration_match.group(1)) if duration_match else None

    just_match = re.search(
        r"Justification:\s*(.*)",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    justification = just_match.group(1).strip() if just_match else None
    return pred_amount, pred_duration, justification


def load_jsonl_predictions_with_justification(jsonl_file, setting, truth_lookup=None):
    rows = []

    with open(jsonl_file, "r") as f:
        for line in f:
            ex = json.loads(line)

            pred_text = ex.get("filtered_resps", [""])[0]
            pred_amount, pred_duration, justification = extract_prediction_and_justification(pred_text)
            
            doc_id = ex.get("doc_id")
            if setting == "factual":
                true_amount = ex.get("doc", {}).get("credit_amount")
                true_duration = ex.get("doc", {}).get("duration")
            else:
                true_amount = truth_lookup.get(doc_id, {}).get("true_amount") if truth_lookup else None
                true_duration = truth_lookup.get(doc_id, {}).get("true_duration") if truth_lookup else None

            rows.append({
                "doc_id": ex.get("doc_id"),
                "gender": ex.get("doc", {}).get("gender"),
                "age": ex.get("doc", {}).get("age"),
                "true_amount": true_amount,
                "pred_amount": pred_amount,
                "true_duration": true_duration,
                "pred_duration": pred_duration,
                "justification": justification,
            })

    return pd.DataFrame(rows).sort_values("doc_id")

def prediction_summary(df):
    return (
        df.assign(
            amount_abs_error=lambda x: (x["pred_amount"] - x["true_amount"]).abs(),
            duration_abs_error=lambda x: (x["pred_duration"] - x["true_duration"]).abs(),
        )
        .groupby(["model", "shot", "setting"])
        .agg(
            amount_mae=("amount_abs_error", "mean"),
            duration_mae=("duration_abs_error", "mean")
        )
        .reset_index()
    )


def kde_in_distribution_1d(
    df,
    true_col,
    pred_col,
    label,
    setting=None,
    figsize=(8, 5),
):
    """
    Fits a 1D KDE on the true values and scores both true and predicted values
    under that true-data KDE.

    Higher log-density = more in-distribution.
    Lower log-density = less in-distribution.
    """

    data = df[[true_col, pred_col]].dropna().copy()
    scaler = StandardScaler()

    X_true = data[[true_col]].to_numpy()
    X_pred = data[[pred_col]].to_numpy()

    X_true_scaled = scaler.fit_transform(X_true)
    X_pred_scaled = scaler.transform(X_pred)

    bandwidths = np.logspace(-1, 1, 20)

    grid = GridSearchCV(
        KernelDensity(kernel="gaussian"),
        {"bandwidth": bandwidths},
        cv=5
    )

    grid.fit(X_true_scaled)
    kde = grid.best_estimator_

    true_log = kde.score_samples(X_true_scaled)
    pred_log = kde.score_samples(X_pred_scaled)

    title_prefix = f"{setting}: " if setting is not None else ""

    plt.figure(figsize=figsize)
    sns.kdeplot(true_log, label=f"True {label}", fill=True)
    sns.kdeplot(pred_log, label=f"Predicted {label}", fill=True)
    plt.xlabel(f"Log density under true {label} KDE")
    plt.ylabel("Density")
    plt.title(f"{title_prefix}In-distribution check for {label}")
    plt.legend()
    plt.tight_layout()
    plt.show()




def compute_treatment_discrimination_measure(
    prompt_type,
    data_name,
    serialization_type,
    discrimination_cols,
    output_directory,
    aggregation_level='overall',
    protected_group=None
):
    """
    Treatment discrimination for one (prompt, dataset, serialization) slice.

    TTD = CF   - F      (Total Treatment Discrimination)
    DTD = PSCF - F      (Direct Treatment Discrimination, per current convention)

    aggregation_level:
      'overall'      -> mean/std of TTD and DTD across all rows.
      'grouplevels'  -> splits by `protected_group` (looked up from data_protected
                        if not passed). Reports TTD and DTD for each group value
                        plus the between-group gap = group1 - group0, where
                        group0/group1 are the two sorted unique values.
    """
    file_path = output_directory / prompt_type / f"{data_name}_{serialization_type}.csv"
    df = pd.read_csv(file_path)

    if protected_group is None:
        protected_group = data_protected.get(data_name)

    rows = []
    for col in discrimination_cols:
        needed = [f"{col}_F", f"{col}_CF", f"{col}_PSCF"]
        if not all(c in df.columns for c in needed):
            print(f"Skipping {col!r}: columns {needed} not all present.")
            continue

        if aggregation_level == 'overall':
            trio = df[needed].apply(pd.to_numeric, errors="coerce").dropna()
            if trio.empty:
                continue
            f  = trio[f"{col}_F"].to_numpy()
            cf = trio[f"{col}_CF"].to_numpy()
            ps = trio[f"{col}_PSCF"].to_numpy()
            ttd, dtd = cf - f, ps - f
            rows.append({
                "treatment": col,
                "n":         len(trio),
                "TTD_mean":  ttd.mean(), "TTD_std": ttd.std(),
                "DTD_mean":  dtd.mean(), "DTD_std": dtd.std(),
            })

        elif aggregation_level == 'grouplevels':
            if not protected_group or protected_group not in df.columns:
                raise ValueError(
                    f"protected_group {protected_group!r} not found in "
                    f"{file_path.name}; pass it explicitly or add it to data_protected."
                )
            keep = df[needed + [protected_group]].copy()
            keep[needed] = keep[needed].apply(pd.to_numeric, errors="coerce")
            keep = keep.dropna(subset=needed + [protected_group])
            uniques = sorted(keep[protected_group].unique(), key=str)
            if len(uniques) < 2:
                print(f"Skipping {col!r} for grouplevels: only {len(uniques)} group "
                    f"value(s) after dropna ({uniques}); rows surviving = {len(keep)}.")
                continue
            if len(uniques) > 2:
                print(f"Warning: {protected_group} has {len(uniques)} unique values "
                    f"({uniques}); gap = last - first after sorting.")
            g0, g1 = uniques[0], uniques[-1]
            def _means(sub):
                f  = sub[f"{col}_F"].to_numpy()
                cf = sub[f"{col}_CF"].to_numpy()
                ps = sub[f"{col}_PSCF"].to_numpy()
                return (cf - f).mean(), (ps - f).mean(), len(sub)
            ttd0, dtd0, n0 = _means(keep[keep[protected_group] == g0])
            ttd1, dtd1, n1 = _means(keep[keep[protected_group] == g1])
            rows.append({
                "treatment":                 col,
                f"n_{protected_group}={g0}": n0,
                f"n_{protected_group}={g1}": n1,
                f"TTD_{protected_group}={g0}": ttd0,
                f"TTD_{protected_group}={g1}": ttd1,
                f"DTD_{protected_group}={g0}": dtd0,
                f"DTD_{protected_group}={g1}": dtd1,
            })
        else:
            raise ValueError(f"Unknown aggregation_level: {aggregation_level!r}")
    summary = pd.DataFrame(rows)
    summary.insert(0, "prompt",        prompt_type)
    summary.insert(1, "dataset",       data_name)
    summary.insert(2, "serialization", serialization_type)
    return summary