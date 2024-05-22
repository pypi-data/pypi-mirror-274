from unittest.mock import Mock

import pytest

from data_ingestion.aws_services import scheduler_service


def test_create_scheduler(scheduler_client):

    response = scheduler_service.create_schedule(
        "test-schedule", "0 0 * * ? *", scheduler_client
    )

    assert response is not None
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert (
        response["ScheduleArn"]
        == "arn:aws:scheduler:ap-southeast-1:123456789012:schedule/default/test-schedule"
    )


def test_create_scheduler_exception(scheduler_client, caplog):
    scheduler_client.create_schedule = Mock(side_effect=Exception("An error occurred"))

    scheduler_service.create_schedule("test-schedule", "0 0 * * ? *", scheduler_client)

    assert "An error occurred" in caplog.text


def test_update_scheduler(scheduler_client):
    scheduler_service.create_schedule("test-schedule", "0 0 * * ? *", scheduler_client)

    response = scheduler_service.update_schedule(
        "test-schedule", "0 10 * * ? *", scheduler_client
    )

    assert response is not None
    assert (
        response["ScheduleArn"]
        == "arn:aws:scheduler:ap-southeast-1:123456789012:schedule/default/test-schedule"
    )

    schedule = scheduler_client.get_schedule(Name="test-schedule")

    assert schedule["ScheduleExpression"] == "cron(0 10 * * ? *)"


def test_update_scheduler_exception(scheduler_client, caplog):
    scheduler_service.update_schedule("test-schedule", "0 0 * * ? *", scheduler_client)

    assert "An error occurred" in caplog.text


def test_delete_scheduler(scheduler_client):
    scheduler_service.create_schedule("test-schedule", "0 0 * * ? *", scheduler_client)

    response = scheduler_service.delete_schedule("test-schedule", scheduler_client)

    assert response is not None
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_delete_scheduler_exception(scheduler_client, caplog):

    scheduler_service.delete_schedule("test-schedule", scheduler_client)

    assert "KeyError" in caplog.text
