from typing import Any, Dict

HMDA_CONFIG: Dict[str, Any] = {
    "known_suffixes": ["_F", "_CF", "_cf"],
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
    }}

    # "path_sensitive_cf_labels": {
    #     "action_taken_TTD": "TTD action taken",
    #     "action_taken_PSDL": "PSDL action taken",
    #     "loan_amount_000s_PSDT": "PSDT loan amount (thousands)",
    #     "preapproval_PSDT": "PSDT preapproval",
    #     "action_taken_PSDT": "PSDT action taken",
    # },
# }