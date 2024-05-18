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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from ri.apiclient.models.testrun_test_category_type import TestrunTestCategoryType
from typing import Optional, Set
from typing_extensions import Self

class TestRunMetricsCategorySummaryMetric(BaseModel):
    """
    CategorySummaryMetric returns a summary metric across test batches for a particular category, such as the average severity for all \"Drift\" tests.
    """ # noqa: E501
    test_category: Optional[TestrunTestCategoryType] = Field(default=None, alias="testCategory")
    category_id: Optional[StrictStr] = Field(default=None, description="The string field `category` is deprecated in v2.1 and will be removed in v2.3. Please use the enum field test_category instead, which provides the same info.", alias="categoryId")
    name: Optional[StrictStr] = Field(default=None, description="The name of the category.")
    value: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The value of the metric over the specified category.")
    __properties: ClassVar[List[str]] = ["testCategory", "categoryId", "name", "value"]

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
        """Create an instance of TestRunMetricsCategorySummaryMetric from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestRunMetricsCategorySummaryMetric from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "testCategory": obj.get("testCategory"),
            "categoryId": obj.get("categoryId"),
            "name": obj.get("name"),
            "value": obj.get("value")
        })
        return _obj


