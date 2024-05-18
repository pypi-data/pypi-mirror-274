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
from ri.apiclient.models.list_metric_identifiers_response_aggregated_metric import ListMetricIdentifiersResponseAggregatedMetric
from ri.apiclient.models.list_metric_identifiers_response_feature_metrics import ListMetricIdentifiersResponseFeatureMetrics
from typing import Optional, Set
from typing_extensions import Self

class RimeListMetricIdentifiersResponse(BaseModel):
    """
    ListMetricIdentifiersResponse returns metric identifiers grouped under features, subsets or neither.
    """ # noqa: E501
    aggregated_metrics: Optional[List[ListMetricIdentifiersResponseAggregatedMetric]] = Field(default=None, alias="aggregatedMetrics")
    feature_metrics: Optional[Dict[str, ListMetricIdentifiersResponseFeatureMetrics]] = Field(default=None, alias="featureMetrics")
    __properties: ClassVar[List[str]] = ["aggregatedMetrics", "featureMetrics"]

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
        """Create an instance of RimeListMetricIdentifiersResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in aggregated_metrics (list)
        _items = []
        if self.aggregated_metrics:
            for _item in self.aggregated_metrics:
                if _item:
                    _items.append(_item.to_dict())
            _dict['aggregatedMetrics'] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in feature_metrics (dict)
        _field_dict = {}
        if self.feature_metrics:
            for _key in self.feature_metrics:
                if self.feature_metrics[_key]:
                    _field_dict[_key] = self.feature_metrics[_key].to_dict()
            _dict['featureMetrics'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RimeListMetricIdentifiersResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "aggregatedMetrics": [ListMetricIdentifiersResponseAggregatedMetric.from_dict(_item) for _item in obj["aggregatedMetrics"]] if obj.get("aggregatedMetrics") is not None else None,
            "featureMetrics": dict(
                (_k, ListMetricIdentifiersResponseFeatureMetrics.from_dict(_v))
                for _k, _v in obj["featureMetrics"].items()
            )
            if obj.get("featureMetrics") is not None
            else None
        })
        return _obj


