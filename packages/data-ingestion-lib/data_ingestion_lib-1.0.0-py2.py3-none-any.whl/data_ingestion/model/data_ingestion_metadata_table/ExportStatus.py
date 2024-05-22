from typing import Optional, Tuple


class ExportStatus:
    def __init__(
        self,
        table_name: str,
        export_type: str,
        export_status: str,
        export_sequence: str,
        export_arn: str = "",
        export_time: Optional[int] = None,
        export_from_time: Optional[int] = None,
        export_to_time: Optional[int] = None,
    ) -> None:
        self.table_name = table_name
        self.export_time = export_time
        self.export_from_time = export_from_time
        self.export_to_time = export_to_time
        self.export_arn = export_arn
        self.export_type = export_type
        self.export_status = export_status
        self.export_sequence = export_sequence

    def partition_key(self) -> dict:
        return {"PK": {"S": f"TABLE#{self.table_name}"}}

    def sort_key(self) -> dict:
        if self.export_time is not None:
            export_time_range = f"0-{self.export_time}"
        else:
            export_time_range = f"{self.export_from_time}-{self.export_to_time}"

        return {"SK": {"S": f"RANGE#{export_time_range}"}}

    def primary_key(self) -> dict:
        return {**self.partition_key(), **self.sort_key()}

    def non_key_attributes(self) -> dict:
        return {
            "export_arn": {"S": self.export_arn},
            "export_type": {"S": self.export_type},
            "export_status": {"S": self.export_status},
            "export_sequence": {"S": self.export_sequence},
            **(
                {"export_time": {"N": str(self.export_time)}}
                if self.export_time is not None
                else {}
            ),
            **(
                {"export_from_time": {"N": str(self.export_from_time)}}
                if self.export_from_time is not None
                else {}
            ),
            **(
                {"export_to_time": {"N": str(self.export_to_time)}}
                if self.export_to_time is not None
                else {}
            ),
        }

    def non_empty_attributes(self) -> dict:
        return {
            k: v
            for (k, v) in self.non_key_attributes().items()
            if ("N" in v and v["N"]) or ("S" in v and v["S"])
        }

    def build_update_expression_with_non_empty_attrs(self) -> Tuple[str, dict]:
        attrs_to_update: list = []
        expression_attr_values: dict = {}
        for key, val in self.non_empty_attributes().items():
            attrs_to_update.append(f"{key} = :{key}")
            expression_attr_values[f":{key}"] = val
        update_expression: str = f"SET {', '.join(attrs_to_update)}"

        return update_expression, expression_attr_values

    def to_dynamodb_item(self) -> dict:
        return {
            **self.primary_key(),
            **self.non_key_attributes(),
        }


def export_status_from_dynamodb_item(item: dict) -> ExportStatus:
    return ExportStatus(
        table_name=item["PK"]["S"].split("#")[1],
        export_time=(int(item["export_time"]["N"]) if "export_time" in item else None),
        export_from_time=(
            int(item["export_from_time"]["N"]) if "export_from_time" in item else None
        ),
        export_to_time=(
            int(item["export_to_time"]["N"]) if "export_to_time" in item else None
        ),
        export_arn=item["export_arn"]["S"] if "export_arn" in item else "",
        export_type=item["export_type"]["S"],
        export_status=item["export_status"]["S"],
        export_sequence=item["export_sequence"]["S"],
    )
