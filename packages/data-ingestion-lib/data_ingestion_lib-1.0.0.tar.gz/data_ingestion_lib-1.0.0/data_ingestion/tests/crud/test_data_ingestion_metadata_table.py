from http import HTTPStatus

import pytest

from data_ingestion.crud.data_ingestion_metadata_table.DataIngestionConfig import (
    add_config,
    add_latest_item,
    get_active_config,
    get_latest_config,
    remove_is_active,
)
from data_ingestion.model.data_ingestion_metadata_table.DataIngestionConfig import (
    DataIngestionConfig,
)

PK = "TABLE_CONFIG#table"
table_name = "table"
cron = "0 0 * * ? *"
ITEM = DataIngestionConfig("test", table_name, "122792905", "enabled", cron)


def test_get_latest_config(dynamodb_client, mock_add_config_record):

    result = get_latest_config(table_name, dynamodb_client)

    assert result is not None
    assert result.table_name == table_name
    assert result.cron == cron


def test_get_latest_config_none(
    dynamodb_client, mock_create_data_ingestion_metadata_table
):

    result = get_latest_config(table_name, dynamodb_client)

    assert result is None


def test_get_latest_config_exception(dynamodb_client):
    with pytest.raises(Exception):
        get_latest_config(table_name, dynamodb_client)


def test_remove_is_active(dynamodb_client, mock_add_config_record):
    result = remove_is_active(ITEM, dynamodb_client)

    config = get_latest_config(table_name, dynamodb_client)

    assert result == HTTPStatus.OK
    assert config is not None
    assert config.is_active is None


def test_is_active_exception(dynamodb_client):

    with pytest.raises(Exception):
        remove_is_active(ITEM, dynamodb_client)


def test_get_active_config(dynamodb_client, mock_add_config_record):

    result = get_active_config("test", dynamodb_client)

    assert result is not None
    assert len(result) == 1
    assert result[0].table_name == table_name
    assert result[0].is_active == "true"


def test_get_active_config_none(
    dynamodb_client, mock_create_data_ingestion_metadata_table
):

    result = get_active_config("test", dynamodb_client)

    assert result == []


def test_get_active_config_exception(dynamodb_client):

    with pytest.raises(Exception):
        get_active_config("test", dynamodb_client)


def test_add_data_ingestion_conflict(dynamodb_client, mock_add_config_record):
    response = add_config(
        ITEM.to_dynamodb_item(),
        dynamodb_client,
    )

    assert response == 409


def test_add_data_ingestion_exception(dynamodb_client):
    with pytest.raises(Exception):
        add_config(ITEM.to_dynamodb_item(), dynamodb_client)


def test_add_latest_item(dynamodb_client, mock_add_config_record):
    result = add_latest_item(table_name, "122792906", dynamodb_client)

    assert result == HTTPStatus.OK


def test_add_latest_item_conflict(dynamodb_client, mock_add_config_record):

    result = add_latest_item(table_name, "122792905", dynamodb_client)

    assert result == HTTPStatus.CONFLICT


def test_add_latest_item_exception(dynamodb_client):

    with pytest.raises(Exception):
        add_latest_item(table_name, "122792906", dynamodb_client)
