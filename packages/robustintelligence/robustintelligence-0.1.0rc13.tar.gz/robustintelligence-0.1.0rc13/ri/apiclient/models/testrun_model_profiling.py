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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from ri.apiclient.models.testrun_custom_metric import TestrunCustomMetric
from typing import Optional, Set
from typing_extensions import Self

class TestrunModelProfiling(BaseModel):
    """
    Specifies configuration values for profiling the model.
    """ # noqa: E501
    nrows_for_summary: Optional[StrictStr] = Field(default=None, description="Number of rows to perform inference on the model if no predictions.", alias="nrowsForSummary")
    nrows_for_feature_importance: Optional[StrictStr] = Field(default=None, description="Number of rows to calculate feature importance over.", alias="nrowsForFeatureImportance")
    metric_configs_json: Optional[StrictStr] = Field(default=None, description="JSON map of metric API names to keyword arguments, which allows configuration of arbitrary metrics.", alias="metricConfigsJson")
    impact_metric: Optional[StrictStr] = Field(default=None, description="Default impact metric.", alias="impactMetric")
    impact_label_threshold: Optional[Union[Annotated[float, Field(le=1, strict=True)], Annotated[int, Field(le=1, strict=True)]]] = Field(default=None, description="Specifies the threshold for measuring model impact using labeled performance metrics instead of prediction metrics, assuming partial labels.", alias="impactLabelThreshold")
    drift_impact_metric: Optional[StrictStr] = Field(default=None, description="Default drift impact metric.", alias="driftImpactMetric")
    subset_summary_metric: Optional[StrictStr] = Field(default=None, description="The subset performance degradation summary metric is calculated by taking the difference between the worst subset degradation and the overall degradation of the configured metric.", alias="subsetSummaryMetric")
    num_feats_for_subset_summary: Optional[StrictStr] = Field(default=None, description="Number of features over which the subset performance degradation summary metric is aggregated.", alias="numFeatsForSubsetSummary")
    custom_metrics: Optional[List[TestrunCustomMetric]] = Field(default=None, description="List of custom metrics.", alias="customMetrics")
    __properties: ClassVar[List[str]] = ["nrowsForSummary", "nrowsForFeatureImportance", "metricConfigsJson", "impactMetric", "impactLabelThreshold", "driftImpactMetric", "subsetSummaryMetric", "numFeatsForSubsetSummary", "customMetrics"]

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
        """Create an instance of TestrunModelProfiling from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in custom_metrics (list)
        _items = []
        if self.custom_metrics:
            for _item in self.custom_metrics:
                if _item:
                    _items.append(_item.to_dict())
            _dict['customMetrics'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestrunModelProfiling from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "nrowsForSummary": obj.get("nrowsForSummary"),
            "nrowsForFeatureImportance": obj.get("nrowsForFeatureImportance"),
            "metricConfigsJson": obj.get("metricConfigsJson"),
            "impactMetric": obj.get("impactMetric"),
            "impactLabelThreshold": obj.get("impactLabelThreshold"),
            "driftImpactMetric": obj.get("driftImpactMetric"),
            "subsetSummaryMetric": obj.get("subsetSummaryMetric"),
            "numFeatsForSubsetSummary": obj.get("numFeatsForSubsetSummary"),
            "customMetrics": [TestrunCustomMetric.from_dict(_item) for _item in obj["customMetrics"]] if obj.get("customMetrics") is not None else None
        })
        return _obj


