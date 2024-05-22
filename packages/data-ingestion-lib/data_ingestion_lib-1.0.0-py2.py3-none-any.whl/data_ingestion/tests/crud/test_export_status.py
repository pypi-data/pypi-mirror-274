from data_ingestion.crud.data_ingestion_metadata_table.ExportStatus import (
    add_export_status,
    get_export_status_by_keys,
    get_last_export_by_table_name,
    update_export_status,
)
from data_ingestion.model.data_ingestion_metadata_table.ExportStatus import (
    export_status_from_dynamodb_item,
)

PK = "TABLE#table"


def test_get_last_export_by_table_name(
    dynamodb_client, mock_create_data_ingestion_metadata_table
):
    item = {
        "PK": {"S": PK},
        "SK": {"S": "RANGE#0-123456"},
        "export_arn": {"S": "arn:aws:glue:us-east-1:123456789012:job/jobname"},
        "export_type": {"S": "FULL_EXPORT"},
        "export_status": {"S": "IN_PROGRESS"},
        "export_sequence": {"S": "export_1"},
    }
    add_export_status(item, dynamodb_client)
    response = get_last_export_by_table_name("table", dynamodb_client)
    assert response is not None
    assert response.table_name == "table"


def test_get_export_status_by_keys(
    dynamodb_client, mock_create_data_ingestion_metadata_table
):
    item = {
        "PK": {"S": PK},
        "SK": {"S": "RANGE#0-1234567"},
        "export_arn": {"S": "arn:aws:glue:us-east-1:123456789012:job/jobname1"},
        "export_type": {"S": "FULL_EXPORT"},
        "export_status": {"S": "IN_PROGRESS"},
        "export_sequence": {"S": "export_1"},
    }
    add_export_status(item, dynamodb_client)

    response = get_export_status_by_keys(PK, "RANGE#0-1234567", dynamodb_client)

    assert response is not None
    assert response.table_name == "table"


def test_update_export_status(
    dynamodb_client, mock_create_data_ingestion_metadata_table
):
    item = {
        "PK": {"S": PK},
        "SK": {"S": "RANGE#0-12345678"},
        "export_arn": {"S": "arn:aws:glue:us-east-1:123456789012:job/jobname"},
        "export_type": {"S": "FULL_EXPORT"},
        "export_status": {"S": "IN_PROGRESS"},
        "export_sequence": {"S": "export_1"},
        "export_time": {"N": "12345678"},
    }
    add_export_status(item, dynamodb_client)
    export_status = export_status_from_dynamodb_item(item)
    export_status.export_status = "COMPLETED"

    update_export_status(export_status, dynamodb_client)

    response = get_export_status_by_keys(PK, "RANGE#0-12345678", dynamodb_client)

    assert response is not None
    assert response.export_status == "COMPLETED"
