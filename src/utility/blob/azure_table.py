"""
Azure Table Storage client for test data management.

Provides IssuerTableClient for managing issuer entities (BIN ranges) in Azure Table Storage.
Follows the utility/blob pattern established by azure_blob.py.
"""

import logging
from typing import List, Dict, Optional

try:
    from azure.data.tables import TableClient, TableEntity
    AZURE_TABLES_AVAILABLE = True
except ImportError:
    AZURE_TABLES_AVAILABLE = False


LOGGER = logging.getLogger("gec.azure_table")


class IssuerTableClient:
    """
    Azure Table Storage client for managing issuer entities (card BIN ranges).
    
    Uses DefaultAzureCredential for authentication (from connection string).
    Provides idempotent setup (delete-then-create) for test data consistency.
    """
    
    def __init__(self, connection_string: str, table_name: str = "issuerrangetable"):
        """
        Initialize Azure Table Storage client.
        
        Args:
            connection_string: Azure Storage connection string
            table_name: Name of the table (default: issuerrangetable)
            
        Raises:
            ImportError: If azure-data-tables is not installed
        """
        if not AZURE_TABLES_AVAILABLE:
            raise ImportError(
                "azure-data-tables package required. Install with: pip install azure-data-tables"
            )
        
        self.connection_string = connection_string
        self.table_name = table_name
        self._client = TableClient.from_connection_string(connection_string, table_name)
        LOGGER.debug(f"IssuerTableClient initialized for table: {table_name}")
    
    def close(self):
        """Close the table client connection."""
        if self._client:
            self._client.close()
            LOGGER.debug("IssuerTableClient connection closed")
    
    def create_entity(self, partition_key: str, row_key: str, entity_data: Dict) -> TableEntity:
        """
        Create or update an entity in the table.
        
        Args:
            partition_key: Partition key (e.g., BIN range prefix)
            row_key: Row key (unique within partition)
            entity_data: Dictionary with entity attributes
            
        Returns:
            Created TableEntity
        """
        entity = TableEntity()
        entity["PartitionKey"] = partition_key
        entity["RowKey"] = row_key
        entity.update(entity_data)
        
        try:
            self._client.create_entity(entity=entity)
            LOGGER.info(f"Entity created: {partition_key}/{row_key}")
        except Exception as e:
            # If entity already exists, update it
            LOGGER.debug(f"Entity exists, updating: {partition_key}/{row_key}")
            self._client.update_entity(entity=entity)
        
        return entity
    
    def delete_entity(self, partition_key: str, row_key: str):
        """
        Delete an entity from the table.
        
        Args:
            partition_key: Partition key
            row_key: Row key
        """
        try:
            self._client.delete_entity(partition_key, row_key)
            LOGGER.info(f"Entity deleted: {partition_key}/{row_key}")
        except Exception as e:
            LOGGER.warning(f"Entity not found (expected if first run): {partition_key}/{row_key}")
    
    def get_entity(self, partition_key: str, row_key: str) -> Optional[TableEntity]:
        """
        Retrieve an entity from the table.
        
        Args:
            partition_key: Partition key
            row_key: Row key
            
        Returns:
            TableEntity or None if not found
        """
        try:
            entity = self._client.get_entity(partition_key, row_key)
            LOGGER.debug(f"Entity retrieved: {partition_key}/{row_key}")
            return entity
        except Exception as e:
            LOGGER.debug(f"Entity not found: {partition_key}/{row_key}")
            return None
    
    def list_entities(self, partition_key: Optional[str] = None) -> List[TableEntity]:
        """
        List all entities in the table (optionally filtered by partition).
        
        Args:
            partition_key: Optional partition key to filter by
            
        Returns:
            List of TableEntity objects
        """
        if partition_key:
            filter_expr = f"PartitionKey eq '{partition_key}'"
            entities = self._client.query_entities(filter_expr)
        else:
            entities = self._client.query_entities()
        
        return list(entities)
    
    def setup_issuer_ranges(self, issuer_entities: List[Dict]):
        """
        Setup issuer range entities (idempotent: delete-then-create).
        
        Each issuer_entity should have:
            - partition_key: BIN range prefix (e.g., "300000", "500000")
            - row_key: Unique identifier within partition
            - issuer_name: Human-readable issuer name
            - bin_start: BIN range start
            - bin_end: BIN range end
            - card_type: Card type (VISA, MASTERCARD, AMEX, etc.)
        
        Args:
            issuer_entities: List of issuer entity dictionaries
        """
        for entity_data in issuer_entities:
            partition_key = entity_data.get("partition_key")
            row_key = entity_data.get("row_key", partition_key)
            
            if not partition_key:
                LOGGER.warning("Issuer entity missing partition_key, skipping")
                continue
            
            # Idempotent: delete first if exists, then create
            self.delete_entity(partition_key, row_key)
            self.create_entity(partition_key, row_key, entity_data)
            LOGGER.info(f"Issuer range setup: {entity_data.get('issuer_name', 'N/A')}")


def build_issuer_table_client(connection_string: str, table_name: str = "issuerrangetable") -> Optional[IssuerTableClient]:
    """
    Factory function to build IssuerTableClient with error handling.
    
    Args:
        connection_string: Azure Storage connection string
        table_name: Table name (default: issuerrangetable)
        
    Returns:
        IssuerTableClient instance or None if initialization fails
    """
    if not connection_string:
        LOGGER.info("No Azure Storage connection string provided - issuer range setup skipped")
        return None
    
    try:
        client = IssuerTableClient(connection_string, table_name)
        LOGGER.info("IssuerTableClient created successfully")
        return client
    except ImportError as e:
        LOGGER.warning(f"Azure Tables not installed: {e}")
        return None
    except Exception as e:
        LOGGER.warning(f"Failed to create IssuerTableClient: {e}")
        return None
