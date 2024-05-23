import pytest

from mutalyzer_spdi_parser.convert import to_hgvs_internal_model, to_spdi_model

TESTS_SET = [
    (
        "NG_012337.3:10:C:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_sequence": "C",
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "deleted": [{"sequence": "C", "source": "description"}],
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:1:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_length": 1,
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10::T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 10},
                    },
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:0:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_length": 0,
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 10},
                    },
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:CT:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_sequence": "CT",
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 12},
                    },
                    "deleted": [{"sequence": "CT", "source": "description"}],
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:2:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_length": 2,
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 12},
                    },
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:2:",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_length": 2,
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 12},
                    },
                    "inserted": [],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:CT:",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_sequence": "CT",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 12},
                    },
                    "deleted": [{"sequence": "CT", "source": "description"}],
                    "inserted": [],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10::",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "inserted": [
                        {
                            "location": {
                                "type": "range",
                                "start": {"type": "point", "position": 10},
                                "end": {"type": "point", "position": 11},
                            },
                            "source": "reference",
                        }
                    ],
                }
            ],
        },
    ),
    (
        "GRCh38(chr11):10::",
        {
            "seq_id": "GRCh38",
            "position": 10,
            "selector": {"id": "chr11"}
        },
        {
            "type": "description_dna",
            "reference": {"id": "GRCh38", "selector": {"id": "chr11"}},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "inserted": [
                        {
                            "location": {
                                "type": "range",
                                "start": {"type": "point", "position": 10},
                                "end": {"type": "point", "position": 11},
                            },
                            "source": "reference",
                        }
                    ],
                }
            ],
        },
    ),
    (
        "NP_003997.1:1:M:RSTV",
        {
            "seq_id": "NP_003997.1",
            "position": 1,
            "deleted_sequence": "M",
            "inserted_sequence": "RSTV",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NP_003997.1"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 1},
                        "end": {"type": "point", "position": 2},
                    },
                    "deleted": [{"sequence": "M", "source": "description"}],
                    "inserted": [{"sequence": "RSTV", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NM_003002.2:273:g:u",
        {
            "seq_id": "NM_003002.2",
            "position": 273,
            "deleted_sequence": "g",
            "inserted_sequence": "u",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NM_003002.2"},
            "variants": [
                {
                    "type": "deletion_insertion",
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 273},
                        "end": {"type": "point", "position": 274},
                    },
                    "deleted": [{"sequence": "g", "source": "description"}],
                    "inserted": [{"sequence": "u", "source": "description"}],
                }
            ],
        },
    ),
]


@pytest.mark.parametrize(
    "description, model",
    [(t[0], t[1]) for t in TESTS_SET],
)
def test_to_spdi_model(description, model):
    assert to_spdi_model(description) == model


@pytest.mark.parametrize(
    "description, model",
    [(t[0], t[2]) for t in TESTS_SET],
)
def test_to_hgvs_internal_model(description, model):
    assert to_hgvs_internal_model(description) == model
