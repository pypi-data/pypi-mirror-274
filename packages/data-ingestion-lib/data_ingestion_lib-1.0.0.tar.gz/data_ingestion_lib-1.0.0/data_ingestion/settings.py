import os

ENV = os.getenv("ENV", "local")

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")

LOCAL_DYNAMODB_ENDPOINT = os.getenv("LOCAL_DYNAMODB_ENDPOINT", "http://localhost:8000")

LOCAL_STEP_FUNCTIONS_ENDPOINT = os.getenv(
    "LOCAL_STEP_FUNCTIONS_ENDPOINT", "http://localhost:8083"
)

DATA_INGESTION_SQS_QUEUE_ARN = os.getenv(
    "DATA_INGESTION_SQS_QUEUE_ARN",
    default="arn:aws:sqs:ap-southeast-1:000000000000:data-ingestion-queue",
)
DATA_INGESTION_DLQ_ARN = os.getenv(
    "DATA_INGESTION_DLQ_ARN",
    default="arn:aws:sqs:ap-southeast-1:000000000000:data-ingestion-dlq",
)
SCHEDULER_ROLE_ARN = os.getenv(
    "SCHEDULER_ROLE_ARN", default="arn:aws:iam::000000000000:role/scheduler-role"
)
DATA_INGESTION_BUCKET = os.getenv(
    "DATA_INGESTION_BUCKET", "data-ingestion.tst.irl.tymebank.co.za"
)
