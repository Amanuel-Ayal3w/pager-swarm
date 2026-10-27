"""Argument schemas. A tool call is validated before it runs."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from pager.safety.allowlist import CONFIG_KEYS, MAX_REPLICAS, check_service


class Args(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Empty(Args):
    pass


class ReadLogs(Args):
    service: str
    limit: int = Field(default=20, ge=1, le=50)

    @field_validator("service")
    @classmethod
    def known(cls, value: str) -> str:
        check_service(value)
        return value


class SearchLogs(Args):
    service: str
    query: str = ""
    limit: int = Field(default=20, ge=1, le=50)

    @field_validator("service")
    @classmethod
    def known(cls, value: str) -> str:
        check_service(value)
        return value


class QueryMetrics(Args):
    service: str

    @field_validator("service")
    @classmethod
    def known(cls, value: str) -> str:
        check_service(value)
        return value


class ListDeploys(Args):
    service: str

    @field_validator("service")
    @classmethod
    def known(cls, value: str) -> str:
        check_service(value)
        return value


class GitDiff(Args):
    deploy_id: str = Field(min_length=1, max_length=64)


class ServiceName(Args):
    service: str

    @field_validator("service")
    @classmethod
    def known(cls, value: str) -> str:
        check_service(value)
        return value


class ScaleService(Args):
    service: str
    replicas: int = Field(ge=1, le=MAX_REPLICAS)

    @field_validator("service")
    @classmethod
    def known(cls, value: str) -> str:
        check_service(value)
        return value


class UpdateConfig(Args):
    service: str
    values: dict[str, bool | int | str]

    @field_validator("service")
    @classmethod
    def known(cls, value: str) -> str:
        check_service(value)
        return value

    @field_validator("values")
    @classmethod
    def allowlisted(cls, value: dict) -> dict:
        unknown = set(value) - CONFIG_KEYS
        if unknown:
            raise ValueError(f"config key is not allowlisted: {', '.join(sorted(unknown))}")
        return value
