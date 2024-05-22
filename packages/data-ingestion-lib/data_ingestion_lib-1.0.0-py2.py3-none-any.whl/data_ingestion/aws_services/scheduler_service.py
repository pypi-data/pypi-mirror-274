"""Contains the EventBridge scheduler service."""

import json

from data_ingestion import settings
from data_ingestion.utils.logger import configure_logging

logger = configure_logging()
SQS_QUEUE_ARN = settings.DATA_INGESTION_SQS_QUEUE_ARN
DLQ_ARN = settings.DATA_INGESTION_DLQ_ARN
SCHEDULER_ROLE_ARN = settings.SCHEDULER_ROLE_ARN


def create_schedule(name: str, schedule_expression: str, scheduler_client):
    try:
        response = scheduler_client.create_schedule(
            Name=name,
            ScheduleExpression=f"cron({schedule_expression})",
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": SQS_QUEUE_ARN,
                "RoleArn": SCHEDULER_ROLE_ARN,
                "Input": json.dumps(
                    {"table_name": name, "schedule_expression": schedule_expression}
                ),
                "DeadLetterConfig": {"Arn": DLQ_ARN},
            },
        )
        return response
    except Exception as ex:
        logger.exception(ex)


def update_schedule(name: str, schedule_expression: str, scheduler_client):
    try:
        response = scheduler_client.update_schedule(
            Name=name,
            ScheduleExpression=f"cron({schedule_expression})",
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": SQS_QUEUE_ARN,
                "RoleArn": SCHEDULER_ROLE_ARN,
                "Input": json.dumps(
                    {"table_name": name, "schedule_expression": schedule_expression}
                ),
                "DeadLetterConfig": {"Arn": DLQ_ARN},
            },
        )
        return response
    except Exception as ex:
        logger.exception(ex)


def delete_schedule(name: str, scheduler_client):
    try:
        response = scheduler_client.delete_schedule(Name=name)
        return response
    except Exception as ex:
        logger.exception(ex)
