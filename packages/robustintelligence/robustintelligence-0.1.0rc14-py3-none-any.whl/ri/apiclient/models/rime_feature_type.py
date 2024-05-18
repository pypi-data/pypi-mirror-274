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
import json
from enum import Enum
from typing_extensions import Self


class RimeFeatureType(str, Enum):
    """
    RimeFeatureType
    """

    """
    allowed enum values
    """
    FEATURE_TYPE_CATEGORICAL = 'FEATURE_TYPE_CATEGORICAL'
    FEATURE_TYPE_NUMERIC_CATEGORICAL = 'FEATURE_TYPE_NUMERIC_CATEGORICAL'
    FEATURE_TYPE_BOOL_CATEGORICAL = 'FEATURE_TYPE_BOOL_CATEGORICAL'
    FEATURE_TYPE_STRING_CATEGORICAL = 'FEATURE_TYPE_STRING_CATEGORICAL'
    FEATURE_TYPE_EMAIL_CATEGORICAL = 'FEATURE_TYPE_EMAIL_CATEGORICAL'
    FEATURE_TYPE_DOMAIN_CATEGORICAL = 'FEATURE_TYPE_DOMAIN_CATEGORICAL'
    FEATURE_TYPE_URL_CATEGORICAL = 'FEATURE_TYPE_URL_CATEGORICAL'
    FEATURE_TYPE_NUMERIC = 'FEATURE_TYPE_NUMERIC'
    FEATURE_TYPE_FLOAT = 'FEATURE_TYPE_FLOAT'
    FEATURE_TYPE_INTEGER = 'FEATURE_TYPE_INTEGER'
    FEATURE_TYPE_MIXED = 'FEATURE_TYPE_MIXED'
    FEATURE_TYPE_EMBEDDING = 'FEATURE_TYPE_EMBEDDING'
    FEATURE_TYPE_TEXT = 'FEATURE_TYPE_TEXT'
    FEATURE_TYPE_IMAGE = 'FEATURE_TYPE_IMAGE'
    FEATURE_TYPE_ENTITIES = 'FEATURE_TYPE_ENTITIES'
    FEATURE_TYPE_BOUNDING_BOXES = 'FEATURE_TYPE_BOUNDING_BOXES'
    FEATURE_TYPE_DATETIME = 'FEATURE_TYPE_DATETIME'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RimeFeatureType from a JSON string"""
        return cls(json.loads(json_str))


