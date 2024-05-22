import yaml
from mypy_boto3_s3 import S3Client

from data_ingestion.utils.logger import configure_logging

logger = configure_logging()


def get_s3_config(bucket: str, key: str, domain: str, s3_client: S3Client):
    """
    Get configuration from s3 file
    """
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        config = yaml.safe_load(body)
        if not config or not config.get(domain, {}):
            return {}
        s3_config = {
            key: value["CronExpression"] for key, value in config[domain].items()
        }
        return s3_config
    except Exception as ex:
        logger.exception(f"Error getting object {key} from bucket {bucket}.")
        raise ex


def get_s3_object(bucket: str, key: str, s3_client: S3Client):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read()
        return body
    except Exception as ex:
        logger.exception(f"Error getting object {key} from bucket {bucket}.")
        raise ex
