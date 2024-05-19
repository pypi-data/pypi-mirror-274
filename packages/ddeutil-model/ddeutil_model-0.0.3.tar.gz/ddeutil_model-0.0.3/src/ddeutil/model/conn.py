# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import (
    Annotated,
    Any,
    Literal,
    Optional,
    Union,
)

from pydantic import Field
from pydantic.functional_validators import field_validator
from pydantic.types import SecretStr
from pydantic_core import Url

from .__base import BaseUpdatableModel
from .__types import CustomUrl, FileUrl
from .utils import unquote_str


class BaseConn(BaseUpdatableModel):
    type: str = "base"


class Conn(BaseConn):
    type: Literal["conn"] = "conn"
    dialect: str
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    pwd: Optional[SecretStr] = None
    endpoint: Optional[str] = None
    options: Annotated[dict[str, Any], Field(default_factory=dict)]

    @classmethod
    def from_url(cls, url: Union[Url, str]) -> Conn:
        if isinstance(url, str):
            url = Url(url=url)
        elif not isinstance(url, Url):
            raise ValueError("A url value must be string or `CustomUrl` object")
        return cls(
            dialect=url.scheme,
            host=unquote_str(url.host),
            port=url.port,
            user=unquote_str(url.username),
            pwd=unquote_str(url.password),
            endpoint=url.path,
            options=dict(url.query_params()),
        )

    @field_validator("endpoint")
    def __check_endpoint_name(cls, v: str) -> str:
        return v.lstrip("/")


class FlConn(BaseConn):
    type: Literal["file"] = "file"
    sys: str
    pointer: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    pwd: Optional[SecretStr] = None
    path: str
    options: Annotated[dict[str, Any], Field(default_factory=dict)]

    @classmethod
    def from_url(cls, url: Union[FileUrl, str]) -> FlConn:
        if isinstance(url, str):
            url = FileUrl(url=url)
        elif not isinstance(url, FileUrl):
            raise ValueError("A url value must be string or `FileUrl` object")
        return cls(
            sys=url.scheme,
            pointer=unquote_str(url.password),
            port=url.port,
            user=unquote_str(url.username),
            pwd=unquote_str(url.password),
            path=url.path,
            options=dict(url.query_params()),
        )


class DbConn(BaseConn):
    """Database Connection Model

    Example:
        *   {
                "type": "db",
                "driver": "sqlite",
            }
    """

    type: Literal["db"] = "db"
    driver: str
    host: str
    port: int
    user: str
    pwd: SecretStr
    db: str
    options: Annotated[dict[str, Any], Field(default_factory=dict)]

    @classmethod
    def from_url(cls, url: Union[CustomUrl, str]) -> DbConn:
        if isinstance(url, str):
            url = CustomUrl(url=url)
        elif not isinstance(url, CustomUrl):
            raise ValueError("A url value must be string or `CustomUrl` object")
        return cls(
            driver=url.scheme,
            host=unquote_str(url.host),
            port=url.port,
            user=unquote_str(url.username),
            pwd=unquote_str(url.password),
            db=url.path,
            options=dict(url.query_params()),
        )

    @field_validator("db")
    def __check_db_name(cls, v: str) -> str:
        return v.lstrip("/").split("/")[0]
