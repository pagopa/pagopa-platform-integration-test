"""GEC issuer range entities for Azure Table setup."""

ISSUER_ENTITIES = [
    {
        "partition_key": "300000",
        "row_key": "1005066",
        "LOW_RANGE": "3095000000000000000",
        "HIGH_RANGE": "3095999999999999999",
        "CIRCUIT": "DINERS",
        "PRODUCT_CODE": "N",
        "PRODUCT_TYPE": "2",
        "PRODUCT_CATEGORY": "C",
        "ISSUER_ID": "100",
        "ABI": "14156"
    },
    {
        "partition_key": "309500",
        "row_key": "1005067",
        "LOW_RANGE": "3095000000000000000",
        "HIGH_RANGE": "3095999999999999999",
        "CIRCUIT": "DINERS",
        "PRODUCT_CODE": "N",
        "PRODUCT_TYPE": "2",
        "PRODUCT_CATEGORY": "C",
        "ISSUER_ID": "100",
        "ABI": "14156",
    },
    {
        "partition_key": "340000",
        "row_key": "321087",
        "LOW_RANGE": "3400000000000000000",
        "HIGH_RANGE": "3499999999999999999",
        "CIRCUIT": "AMEX",
        "PRODUCT_CODE": "99",
        "PRODUCT_TYPE": "3",
        "PRODUCT_CATEGORY": "C",
        "ISSUER_ID": "999999",
        "ABI": "AMREX",
    },
]
