"""This file contains common constants used across the project."""

from enum import Enum

DATA_INGESTION_METADATA_TABLE = "data-ingestion-metadata"
DATA_INGESTION_EVENT_BUS = "tp-data-ingestion-event-bus"


class DBExportStatus(Enum):
    """
    Enum for export status
    """

    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ExportType(Enum):
    FULL_EXPORT = "FULL_EXPORT"
    INCREMENTAL_EXPORT = "INCREMENTAL_EXPORT"


class ConfigStatus(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
