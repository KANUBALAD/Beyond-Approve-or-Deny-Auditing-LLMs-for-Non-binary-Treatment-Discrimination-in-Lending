from typing import Any, Dict


GERMAN_CONFIG: Dict[str, Any] = {
    "known_suffixes": ["_F", "_CF", "_cf"],
    "drop_from_main_json": [],

    "feature_labels": {
        "gender": "gender",
        "age": "age",
        "checking_status": "checking status",
        "credit_history": " credit history",
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

    "value_maps": {
        "gender": {
            0: "female",
            1: "male",
        },
        "checking_status": {
            0: "a checking account with less than 200 Deutsche Mark",
            1: "a checking account with 0 Deutsche Mark",
            2: "a checking account with 200 Deutsche Mark or more",
            3: "no checking account",
        },
        "credit_history": {
            0: "has duly paid back credits received from this bank till now",
            1: "has critical account or has other credits existing but not at this bank",
            2: "has delayed paying back credits received from this bank in the past",
            3: "has duly paid back all credits at this bank",
            4: "did not take any credits at this bank or has duly paid back all credits at this bank",
        },
        "purpose": {
            0: 'domestic appliance',
            1: 'new car',
            2: 'used car',
            3: 'business',
            4: 'education',
            5: 'furniture/equipment',
            6: 'other',
            7: 'radio/tv',
            8: 'repairs',
            9: 'retraining'
        },

        "savings_status":{
        0: 'a savings with more than 100 Deutsche Mark but less than 500 Deutsche Mark',
        1: 'a savings with more than 500 Deutsche Mark but less than 1000 Deutsche Mark',
        2: 'a savings acccount with less than 100 Deutsche Mark',
        3: 'a savings with 1000 Deutsche Mark or more',
        4: 'no known savings'},
                
        "employment": {
            0: 'employed for more than one year but less than four years',
            1: 'employed for more than four years but less than seven years',
            2: 'employed for less than one years',
            3: 'employed for more than seven years',
            4: 'unemployed'
        },
        "other_parties": {
            0: "co applicant",
            1: "guarantor",
            2: "no guarantor",
        },
        "property_magnitude": {
            0: 'life insurance',
            1: 'no known property',
            2: 'some real estate property',
            3: 'car'
        },
        "other_payment_plans": {
            0: "bank",
            1: "none",
            2: "stores",
        },
        "housing": {
            0: 'free accommodation',
            1: 'self-owned house',
            2: 'rented apartment or house',
        },
        "job": {
            0: 'high qualified or self employed or has managerial position',
            1: 'unemployed and unskilled non resident',
            2: 'unskilled resident',
            3: 'skilled'
        },
        "own_telephone": {
            0: "none",
            1: "yes",
        },
        "foreign_worker": {
            0: "no",
            1: "yes",
        },
        "class": {
            0: "bad",
            1: "good",
        },
    },

}