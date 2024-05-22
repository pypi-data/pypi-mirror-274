from data_ingestion.utils import (
    datetime_util,
    aws_session,
    dynamodb_client,
    eventbridge_client,
    s3_client,
    sqs_client,
    step_function_client,
    scheduler_client
)


def test_datetime_util():
    current_dt = datetime_util.get_current_datetime()
    current_dt_ms = datetime_util.get_current_timestamp_ms()
    current_dt_from_timestamp = datetime_util.get_datetime_from_timestamp_ms(
        current_dt_ms
    )
    current_timestamp_ms_from_dt = datetime_util.get_timestamp_ms_from_datetime(
        current_dt_from_timestamp
    )
    assert current_dt <= datetime_util.get_current_datetime()
    assert isinstance(current_dt_ms, int)
    assert current_dt_from_timestamp < current_dt
    assert current_timestamp_ms_from_dt == current_dt_ms


def test_aws_session():
    assert aws_session.create_custom_session() is not None


def test_aws_client():
    s3_test_client = s3_client.create_s3_client()
    scheduler_test_client = scheduler_client.create_scheduler_client()
    sqs_test_client = sqs_client.create_sqs_client()
    sf_test_client = step_function_client.create_step_functions_client()
    dynamodb_test_client = dynamodb_client.create_dynamodb_client()
    eventbridge_test_client = eventbridge_client.create_eventbridge_client()
    
    assert s3_test_client is not None
    assert scheduler_test_client is not None
    assert sqs_test_client is not None
    assert sf_test_client is not None
    assert dynamodb_test_client is not None
    assert eventbridge_test_client is not None
