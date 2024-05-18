# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.integration_integration_level import IntegrationIntegrationLevel
from ri.apiclient.models.integration_integration_schema import IntegrationIntegrationSchema
from ri.apiclient.models.integration_integration_type import IntegrationIntegrationType
from ri.apiclient.models.rime_uuid import RimeUUID
from typing import Optional, Set
from typing_extensions import Self

class RischemaintegrationIntegration(BaseModel):
    """
    Integration object in RIME.
    """ # noqa: E501
    id: Optional[RimeUUID] = None
    workspace_id: Optional[RimeUUID] = Field(default=None, alias="workspaceId")
    creation_time: Optional[datetime] = Field(default=None, alias="creationTime")
    name: Optional[StrictStr] = None
    type: Optional[IntegrationIntegrationType] = None
    var_schema: Optional[IntegrationIntegrationSchema] = Field(default=None, alias="schema")
    level: Optional[IntegrationIntegrationLevel] = None
    __properties: ClassVar[List[str]] = ["id", "workspaceId", "creationTime", "name", "type", "schema", "level"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RischemaintegrationIntegration from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of id
        if self.id:
            _dict['id'] = self.id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of workspace_id
        if self.workspace_id:
            _dict['workspaceId'] = self.workspace_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of var_schema
        if self.var_schema:
            _dict['schema'] = self.var_schema.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RischemaintegrationIntegration from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": RimeUUID.from_dict(obj["id"]) if obj.get("id") is not None else None,
            "workspaceId": RimeUUID.from_dict(obj["workspaceId"]) if obj.get("workspaceId") is not None else None,
            "creationTime": obj.get("creationTime"),
            "name": obj.get("name"),
            "type": obj.get("type"),
            "schema": IntegrationIntegrationSchema.from_dict(obj["schema"]) if obj.get("schema") is not None else None,
            "level": obj.get("level")
        })
        return _obj


