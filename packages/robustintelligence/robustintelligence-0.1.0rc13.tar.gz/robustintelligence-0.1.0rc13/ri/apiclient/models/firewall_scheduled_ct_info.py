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
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.registry_data_info import RegistryDataInfo
from ri.apiclient.models.registry_pred_info import RegistryPredInfo
from ri.apiclient.models.rime_uuid import RimeUUID
from typing import Optional, Set
from typing_extensions import Self

class FirewallScheduledCTInfo(BaseModel):
    """
    FirewallScheduledCTInfo
    """ # noqa: E501
    eval_data_integration_id: Optional[RimeUUID] = Field(default=None, alias="evalDataIntegrationId")
    eval_data_info: Optional[RegistryDataInfo] = Field(default=None, alias="evalDataInfo")
    eval_pred_integration_id: Optional[RimeUUID] = Field(default=None, alias="evalPredIntegrationId")
    eval_pred_info: Optional[RegistryPredInfo] = Field(default=None, alias="evalPredInfo")
    last_ct_scheduled: Optional[datetime] = Field(default=None, description="Specifies a timestamp based on the end time of the window for each run. The scheduler uses this timestamp to determine job start times and the time bin to use.", alias="lastCtScheduled")
    activated_time: Optional[datetime] = Field(default=None, description="When the AI Firewall has no bins, this value is used as the start time. Otherwise, the end time of the last bin in the AI Firewall is used as the AI Firewall start time.", alias="activatedTime")
    disable_scheduled_ct: Optional[StrictBool] = Field(default=None, description="Option for disabling scheduled CT - this should be false by default. This enables users to suspend a scheduled CT while preserving existing settings.", alias="disableScheduledCt")
    __properties: ClassVar[List[str]] = ["evalDataIntegrationId", "evalDataInfo", "evalPredIntegrationId", "evalPredInfo", "lastCtScheduled", "activatedTime", "disableScheduledCt"]

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
        """Create an instance of FirewallScheduledCTInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of eval_data_integration_id
        if self.eval_data_integration_id:
            _dict['evalDataIntegrationId'] = self.eval_data_integration_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of eval_data_info
        if self.eval_data_info:
            _dict['evalDataInfo'] = self.eval_data_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of eval_pred_integration_id
        if self.eval_pred_integration_id:
            _dict['evalPredIntegrationId'] = self.eval_pred_integration_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of eval_pred_info
        if self.eval_pred_info:
            _dict['evalPredInfo'] = self.eval_pred_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of FirewallScheduledCTInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "evalDataIntegrationId": RimeUUID.from_dict(obj["evalDataIntegrationId"]) if obj.get("evalDataIntegrationId") is not None else None,
            "evalDataInfo": RegistryDataInfo.from_dict(obj["evalDataInfo"]) if obj.get("evalDataInfo") is not None else None,
            "evalPredIntegrationId": RimeUUID.from_dict(obj["evalPredIntegrationId"]) if obj.get("evalPredIntegrationId") is not None else None,
            "evalPredInfo": RegistryPredInfo.from_dict(obj["evalPredInfo"]) if obj.get("evalPredInfo") is not None else None,
            "lastCtScheduled": obj.get("lastCtScheduled"),
            "activatedTime": obj.get("activatedTime"),
            "disableScheduledCt": obj.get("disableScheduledCt")
        })
        return _obj


