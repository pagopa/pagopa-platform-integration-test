"""
GEC-specific issuer entity definitions for Azure Table Storage.

This module maintains the test data (ISSUER_ENTITIES) used by GEC tests.
The actual Azure Table Storage connectivity is handled by src.utility.blob.azure_table.
"""

# Pre-defined issuer entities for GEC testing
# These define BIN ranges for card routing and validation
# Format: PartitionKey (BIN prefix) + entity data with LOW_RANGE/HIGH_RANGE/CIRCUIT info
ISSUER_ENTITIES = [
    {
        "PartitionKey": "300000",
        "RowKey": "1005066",
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
        "PartitionKey": "500000",
        "RowKey": "1005067",
        "LOW_RANGE": "5000000000000000000",
        "HIGH_RANGE": "5099999999999999999",
        "CIRCUIT": "MASTERCARD",
        "PRODUCT_CODE": "C",
        "PRODUCT_TYPE": "1",
        "PRODUCT_CATEGORY": "C",
        "ISSUER_ID": "200",
        "ABI": "05000"
    },
    {
        "PartitionKey": "600000",
        "RowKey": "1005068",
        "LOW_RANGE": "6000000000000000000",
        "HIGH_RANGE": "6099999999999999999",
        "CIRCUIT": "VISA",
        "PRODUCT_CODE": "C",
        "PRODUCT_TYPE": "1",
        "PRODUCT_CATEGORY": "C",
        "ISSUER_ID": "300",
        "ABI": "02008"
    }
]
