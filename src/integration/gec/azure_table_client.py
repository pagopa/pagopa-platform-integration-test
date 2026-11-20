"""Azure Table Storage client for issuer range management in GEC tests."""

import logging
from typing import Dict, List, Optional

try:
    from azure.data.tables import TableClient
except ImportError:
    TableClient = None

LOGGER = logging.getLogger("gec.azure")


class IssuerTableClient:
    """Manages issuer range entities in Azure Table Storage."""

    def __init__(self, connection_string: str, table_name: str = "pagopadweuafmsaissuerrangetable"):
        """Initialize Azure Table Storage client.
        
        Args:
            connection_string: Azure Storage connection string
            table_name: Name of the table (default: AFM issuer range table)
        
        Raises:
            ImportError: If azure-data-tables is not installed
            Exception: If connection fails
        """
        if TableClient is None:
            raise ImportError(
                "azure-data-tables package is required. Install with: pip install azure-data-tables"
            )
        
        try:
            self.table_client = TableClient.from_connection_string(
                connection_string, table_name
            )
            self.table_name = table_name
            LOGGER.info(f"Azure Table Storage client initialized for table: {table_name}")
        except Exception as e:
            LOGGER.error(f"Failed to initialize Azure Table Storage client: {e}")
            raise

    def setup_issuer_entity(self, entity: Dict) -> None:
        """Setup issuer entity (delete if exists, then create).
        
        Args:
            entity: Entity dict with partitionKey and rowKey
        """
        partition_key = entity.get("PartitionKey") or entity.get("partitionKey")
        row_key = entity.get("RowKey") or entity.get("rowKey")
        
        if not partition_key or not row_key:
            raise ValueError("Entity must have PartitionKey and RowKey")
        
        # Normalize key names for Azure SDK
        entity_normalized = {k: v for k, v in entity.items()}
        entity_normalized["PartitionKey"] = partition_key
        entity_normalized["RowKey"] = row_key
        
        try:
            # Try to delete existing
            try:
                self.table_client.delete_entity(partition_key, row_key)
                LOGGER.debug(f"Deleted existing entity: {partition_key}/{row_key}")
            except Exception:
                pass  # Entity might not exist
            
            # Create new
            self.table_client.create_entity(entity_normalized)
            LOGGER.info(f"Issuer entity created: {partition_key}/{row_key}")
        except Exception as e:
            LOGGER.error(f"Failed to setup issuer entity {partition_key}/{row_key}: {e}")
            raise

    def delete_by_partition_key(self, partition_key: str) -> None:
        """Delete all entities with given partition key.
        
        Args:
            partition_key: Partition key to filter by
        """
        if not partition_key:
            return
        
        try:
            filter_cond = f"PartitionKey eq '{partition_key}'"
            entities = self.table_client.query_entities(filter_cond)
            
            count = 0
            for entity in entities:
                self.table_client.delete_entity(
                    entity["PartitionKey"], entity["RowKey"]
                )
                count += 1
            
            LOGGER.info(f"Deleted {count} entities for partition: {partition_key}")
        except Exception as e:
            LOGGER.error(f"Failed to delete entities for partition {partition_key}: {e}")
            raise


# Pre-defined issuer entities for GEC testing
# These define BIN ranges for card routing and validation
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


def setup_issuer_ranges(connection_string: Optional[str]) -> Optional[IssuerTableClient]:
    """Setup issuer ranges in Azure Table Storage.
    
    Args:
        connection_string: Azure Storage connection string (or None to skip)
    
    Returns:
        IssuerTableClient if setup successful, None if skipped
    """
    if not connection_string:
        LOGGER.warning("No Azure Storage connection string provided - issuer ranges will not be loaded")
        return None
    
    try:
        client = IssuerTableClient(connection_string)
        
        for entity in ISSUER_ENTITIES:
            client.setup_issuer_entity(entity)
        
        LOGGER.info(f"Successfully setup {len(ISSUER_ENTITIES)} issuer entities")
        return client
    except Exception as e:
        LOGGER.error(f"Failed to setup issuer ranges: {e}")
        raise
