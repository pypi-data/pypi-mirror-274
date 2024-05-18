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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from ri.apiclient.models.list_metric_identifiers_response_feature_metric_without_subsets import ListMetricIdentifiersResponseFeatureMetricWithoutSubsets
from ri.apiclient.models.list_metric_identifiers_response_subset_metrics import ListMetricIdentifiersResponseSubsetMetrics
from typing import Optional, Set
from typing_extensions import Self

class ListMetricIdentifiersResponseFeatureMetrics(BaseModel):
    """
    ListMetricIdentifiersResponseFeatureMetrics
    """ # noqa: E501
    feature_metric_without_subsets: Optional[List[ListMetricIdentifiersResponseFeatureMetricWithoutSubsets]] = Field(default=None, alias="featureMetricWithoutSubsets")
    subset_metrics: Optional[Dict[str, ListMetricIdentifiersResponseSubsetMetrics]] = Field(default=None, alias="subsetMetrics")
    __properties: ClassVar[List[str]] = ["featureMetricWithoutSubsets", "subsetMetrics"]

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
        """Create an instance of ListMetricIdentifiersResponseFeatureMetrics from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in feature_metric_without_subsets (list)
        _items = []
        if self.feature_metric_without_subsets:
            for _item in self.feature_metric_without_subsets:
                if _item:
                    _items.append(_item.to_dict())
            _dict['featureMetricWithoutSubsets'] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in subset_metrics (dict)
        _field_dict = {}
        if self.subset_metrics:
            for _key in self.subset_metrics:
                if self.subset_metrics[_key]:
                    _field_dict[_key] = self.subset_metrics[_key].to_dict()
            _dict['subsetMetrics'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ListMetricIdentifiersResponseFeatureMetrics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "featureMetricWithoutSubsets": [ListMetricIdentifiersResponseFeatureMetricWithoutSubsets.from_dict(_item) for _item in obj["featureMetricWithoutSubsets"]] if obj.get("featureMetricWithoutSubsets") is not None else None,
            "subsetMetrics": dict(
                (_k, ListMetricIdentifiersResponseSubsetMetrics.from_dict(_v))
                for _k, _v in obj["subsetMetrics"].items()
            )
            if obj.get("subsetMetrics") is not None
            else None
        })
        return _obj


