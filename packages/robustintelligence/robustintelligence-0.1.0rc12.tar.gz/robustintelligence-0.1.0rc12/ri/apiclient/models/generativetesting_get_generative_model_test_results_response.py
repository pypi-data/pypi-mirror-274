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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.generativetesting_generative_testing_result import GenerativetestingGenerativeTestingResult
from ri.apiclient.models.rime_uuid import RimeUUID
from ri.apiclient.models.statedb_job_status import StatedbJobStatus
from typing import Optional, Set
from typing_extensions import Self

class GenerativetestingGetGenerativeModelTestResultsResponse(BaseModel):
    """
    GenerativetestingGetGenerativeModelTestResultsResponse
    """ # noqa: E501
    results: Optional[List[GenerativetestingGenerativeTestingResult]] = Field(default=None, description="The list of generative testing results.")
    next_page_token: Optional[StrictStr] = Field(default=None, description="A token representing the next page from the list returned by a query.", alias="nextPageToken")
    has_more: Optional[StrictBool] = Field(default=None, description="A Boolean flag that specifies whether there are more results to return.", alias="hasMore")
    job_id: Optional[RimeUUID] = Field(default=None, alias="jobId")
    job_status: Optional[StatedbJobStatus] = Field(default=None, alias="jobStatus")
    __properties: ClassVar[List[str]] = ["results", "nextPageToken", "hasMore", "jobId", "jobStatus"]

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
        """Create an instance of GenerativetestingGetGenerativeModelTestResultsResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in results (list)
        _items = []
        if self.results:
            for _item in self.results:
                if _item:
                    _items.append(_item.to_dict())
            _dict['results'] = _items
        # override the default output from pydantic by calling `to_dict()` of job_id
        if self.job_id:
            _dict['jobId'] = self.job_id.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GenerativetestingGetGenerativeModelTestResultsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "results": [GenerativetestingGenerativeTestingResult.from_dict(_item) for _item in obj["results"]] if obj.get("results") is not None else None,
            "nextPageToken": obj.get("nextPageToken"),
            "hasMore": obj.get("hasMore"),
            "jobId": RimeUUID.from_dict(obj["jobId"]) if obj.get("jobId") is not None else None,
            "jobStatus": obj.get("jobStatus")
        })
        return _obj


