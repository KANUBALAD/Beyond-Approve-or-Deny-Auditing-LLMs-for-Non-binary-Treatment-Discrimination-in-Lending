from __future__ import annotations

from typing import Any, Dict


DATASET_CONFIGS: Dict[str, Dict[str, Any]] = {
    "german": {
        "factual_suffix": "_F",
        "counterfactual_suffix": "_CF",
        "drop_from_main_json": [],

        # Human-readable feature names
        "feature_labels": {
            "gender": "gender",
            "age": "age",
            "checking_status": "checking status",
            "credit_history": "credit history",
            "purpose": "purpose",
            "savings_status": "savings status",
            "employment": "employment",
            "other_parties": "other parties",
            "residence_since": "residence since",
            "property_magnitude": "property magnitude",
            "other_payment_plans": "other payment plans",
            "housing": "housing",
            "existing_credits": "existing credits",
            "job": "job",
            "num_dependents": "number of dependents",
            "own_telephone": "own telephone",
            "foreign_worker": "foreign worker",
            "duration": "duration",
            "credit_amount": "credit amount",
            "installment_commitment": "installment commitment",
            "class": "class",
        },

        # Mappings for coded values.
        # Edit any mapping here if your preprocessing used a different encoding.
        "value_maps": {
            "gender": {
                0: "female",
                1: "male",
            },
            "checking_status": {
                0: "no checking account",
                1: "checking account with balance below 0 DM",
                2: "checking account with balance between 0 and 200 DM",
                3: "checking account with balance at least 200 DM",
            },
            "credit_history": {
                0: "no credits or all credits paid back",
                1: "all credits at this bank paid back",
                2: "existing credits paid back duly till now",
                3: "delay in paying back previous credits",
                4: "critical account or other existing credit",
            },
            "purpose": {
                0: "radio/TV",
                1: "education",
                2: "furniture/equipment",
                3: "car",
                4: "business",
                5: "domestic appliances",
                6: "repairs",
                7: "vacation or other purposes",
            },
            "savings_status": {
                0: "no known savings",
                1: "savings below 100 DM",
                2: "savings between 100 and 500 DM",
                3: "savings between 500 and 1000 DM",
                4: "savings at least 1000 DM",
            },
            "employment": {
                0: "unemployed",
                1: "employed for less than 1 year",
                2: "employed for 1 to less than 4 years",
                3: "employed for 4 to less than 7 years",
                4: "employed for at least 7 years",
            },
            "other_parties": {
                0: "none",
                1: "co-applicant",
                2: "guarantor",
            },
            "property_magnitude": {
                0: "real estate",
                1: "life insurance",
                2: "car or other vehicle",
                3: "no known property",
            },
            "other_payment_plans": {
                0: "bank",
                1: "none",
                2: "stores",
            },
            "housing": {
                0: "rent",
                1: "own",
                2: "for free",
            },
            "job": {
                0: "unemployed or unskilled non-resident",
                1: "unskilled resident",
                2: "skilled employee or official",
                3: "highly qualified employee, self-employed, or management",
            },
            "own_telephone": {
                0: "no",
                1: "yes",
            },
            "foreign_worker": {
                0: "no",
                1: "yes",
            },
            "class": {
                0: "good credit risk",
                1: "bad credit risk",
            },
        },

        # Derived columns that are not factual/counterfactual pairs
        "path_sensitive_cf_labels": {
            "duration_PSTD": "PSTD duration",
            "credit_amount_PSTD": "PSTD credit amount",
            "installment_commitment_PSTD": "PSTD installment commitment",
            "class_PSTD": "PSTD class",
            "class_PSTI": "PSTI class",
            "class_PSDL": "PSDL class",
            "duration_PSDT": "PSDT duration",
            "credit_amount_PSDT": "PSDT credit amount",
            "installment_commitment_PSDT": "PSDT installment commitment",
            "class_PSDT": "PSDT class",
        },
    },
    
    "hmda_ny": {
    "factual_suffix": "_F",
    "counterfactual_suffix": "_CF",
    "drop_from_main_json": [],

    "feature_labels": {
        "applicant_sex": "applicant sex",
        "applicant_race_1": "applicant race",
        "loan_type": "loan type",
        "property_type": "property type",
        "loan_purpose": "loan purpose",
        "owner_occupancy": "owner occupancy",
        "msamd": "MSA/MD code",
        "census_tract_number": "census tract number",
        "applicant_income_000s": "applicant income (thousands)",
        "purchaser_type": "purchaser type",
        "hud_median_family_income": "HUD median family income",
        "tract_to_msamd_income": "tract to MSA/MD income ratio",
        "number_of_owner_occupied_units": "number of owner occupied units",
        "number_of_1_to_4_family_units": "number of 1 to 4 family units",
        "loan_amount_000s": "loan amount (thousands)",
        "preapproval": "preapproval",
        "action_taken": "action taken",
    },

    "value_maps": {
        # Safe because you explicitly binarized them
        "applicant_sex": {
            0: "female",
            1: "male",
        },
        "applicant_race_1": {
            0: "non-White",
            1: "White",
        },
        "action_taken": {
            0: "denied or not originated",
            1: "approved and originated",
        },
    },

    "path_sensitive_cf_labels": {
        "action_taken_TTD": "TTD action taken",
        "action_taken_PSDL": "PSDL action taken",
        "loan_amount_000s_PSDT": "PSDT loan amount (thousands)",
        "preapproval_PSDT": "PSDT preapproval",
        "action_taken_PSDT": "PSDT action taken",
    },
},
    
    
    
    "hmda_tx": {
    "factual_suffix": "_F",
    "counterfactual_suffix": "_CF",
    "drop_from_main_json": [],

    "feature_labels": {
        "applicant_sex": "applicant sex",
        "applicant_race_1": "applicant race",
        "loan_type": "loan type",
        "property_type": "property type",
        "loan_purpose": "loan purpose",
        "owner_occupancy": "owner occupancy",
        "msamd": "MSA/MD code",
        "census_tract_number": "census tract number",
        "applicant_income_000s": "applicant income (thousands)",
        "purchaser_type": "purchaser type",
        "hud_median_family_income": "HUD median family income",
        "tract_to_msamd_income": "tract to MSA/MD income ratio",
        "number_of_owner_occupied_units": "number of owner occupied units",
        "number_of_1_to_4_family_units": "number of 1 to 4 family units",
        "loan_amount_000s": "loan amount (thousands)",
        "preapproval": "preapproval",
        "action_taken": "action taken",
    },

    "value_maps": {
        # Safe because you explicitly binarized them
        "applicant_sex": {
            0: "female",
            1: "male",
        },
        "applicant_race_1": {
            0: "non-White",
            1: "White",
        },
        "action_taken": {
            0: "denied or not originated",
            1: "approved and originated",
        },
    },

    "path_sensitive_cf_labels": {
        "action_taken_TTD": "TTD action taken",
        "action_taken_PSDL": "PSDL action taken",
        "loan_amount_000s_PSDT": "PSDT loan amount (thousands)",
        "preapproval_PSDT": "PSDT preapproval",
        "action_taken_PSDT": "PSDT action taken",
    },
}
    
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

    # Try exact key match after pythonization
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
    
    