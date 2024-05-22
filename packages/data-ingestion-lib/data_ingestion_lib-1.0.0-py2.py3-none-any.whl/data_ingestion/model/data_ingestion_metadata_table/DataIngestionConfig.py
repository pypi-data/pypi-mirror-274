from typing import Optional


class DataIngestionConfig:
    def __init__(
        self,
        domain_name: str,
        table_name: str,
        config_timestamp: str,
        status: Optional[str],
        cron: Optional[str],
        is_active: Optional[str] = None,
    ):
        self.domain_name = domain_name
        self.table_name = table_name
        self.cron = cron
        self.status = status
        self.config_timestamp = config_timestamp
        self.is_active = is_active

    def partition_key(self) -> dict:
        return {"PK": {"S": f"TABLE_CONFIG#{self.table_name}"}}

    def sort_key(self) -> dict:
        return {"SK": {"S": f"CONFIGTIME#{self.config_timestamp}"}}

    def primary_key(self) -> dict:
        return {**self.partition_key(), **self.sort_key()}

    def non_key_attributes(self) -> dict:
        return {
            **({"cron": {"S": self.cron}} if self.cron is not None else {}),
            **({"status": {"S": self.status}} if self.status is not None else {}),
            "domain_file": {"S": self.domain_name},
            **({"is_active": {"S": "true"}} if self.is_active is not None else {}),
        }

    def to_dynamodb_item(self) -> dict:
        return {
            **self.partition_key(),
            **self.sort_key(),
            **self.non_key_attributes(),
        }


def config_from_dynamodb_item(item: dict) -> DataIngestionConfig:
    return DataIngestionConfig(
        domain_name=item["domain_file"]["S"],
        table_name=item["PK"]["S"].split("#")[1],
        cron=(item["cron"]["S"] if "cron" in item else None),
        status=(item["status"]["S"] if "status" in item else None),
        config_timestamp=item["SK"]["S"].split("#")[1],
        is_active=(item["is_active"]["S"] if "is_active" in item else None),
    )
