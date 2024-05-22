import logging
import os
import sys
from datetime import datetime

from pythonjsonlogger import jsonlogger

FORMAT = (
    "%(asctime)s [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] "
    "%(levelname)s - %(message)s"
)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        log_record["tracking_id"] = os.getenv("EXPORT_TRACKING_ID", "")
        log_record["table_name"] = os.getenv("TABLE_NAME", "")
        log_record["export_time_range"] = os.getenv("EXPORT_TIME_RANGE", "")


def configure_handler() -> logging.StreamHandler:
    stdout_handler = logging.StreamHandler(sys.stdout)
    json_formatter = CustomJsonFormatter(FORMAT)
    stdout_handler.setFormatter(json_formatter)

    return stdout_handler


def configure_logging() -> logging.Logger:
    log_handler: logging.StreamHandler = configure_handler()
    root_logger = logging.getLogger()
    # remove the pre-configured handler of AWS Lambda runtime
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(log_handler)

    return root_logger
