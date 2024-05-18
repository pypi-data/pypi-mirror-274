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
from ri.apiclient.models.libgenerative_severity import LibgenerativeSeverity
from ri.apiclient.models.rime_file_security_report import RimeFileSecurityReport
from typing import Optional, Set
from typing_extensions import Self

class RimeFileScanResult(BaseModel):
    """
    RimeFileScanResult
    """ # noqa: E501
    result_update_time: Optional[datetime] = Field(default=None, description="The time when the result was updated.", alias="resultUpdateTime")
    file_security_reports: Optional[List[RimeFileSecurityReport]] = Field(default=None, description="The security reports for the files that were scanned.", alias="fileSecurityReports")
    unscanned_file_paths: Optional[List[StrictStr]] = Field(default=None, description="The list of files that were not scanned.", alias="unscannedFilePaths")
    severity: Optional[LibgenerativeSeverity] = None
    __properties: ClassVar[List[str]] = ["resultUpdateTime", "fileSecurityReports", "unscannedFilePaths", "severity"]

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
        """Create an instance of RimeFileScanResult from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in file_security_reports (list)
        _items = []
        if self.file_security_reports:
            for _item in self.file_security_reports:
                if _item:
                    _items.append(_item.to_dict())
            _dict['fileSecurityReports'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RimeFileScanResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "resultUpdateTime": obj.get("resultUpdateTime"),
            "fileSecurityReports": [RimeFileSecurityReport.from_dict(_item) for _item in obj["fileSecurityReports"]] if obj.get("fileSecurityReports") is not None else None,
            "unscannedFilePaths": obj.get("unscannedFilePaths"),
            "severity": obj.get("severity")
        })
        return _obj


