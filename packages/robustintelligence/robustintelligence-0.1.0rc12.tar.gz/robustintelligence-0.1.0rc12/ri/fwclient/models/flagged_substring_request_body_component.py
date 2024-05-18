# coding: utf-8

"""
    Robust Intelligence Firewall REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Api-Key` header.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class FlaggedSubstringRequestBodyComponent(str, Enum):
    """
    FlaggedSubstringRequestBodyComponent
    """

    """
    allowed enum values
    """
    REQUEST_BODY_COMPONENT_UNSPECIFIED = 'REQUEST_BODY_COMPONENT_UNSPECIFIED'
    REQUEST_BODY_COMPONENT_USER_INPUT = 'REQUEST_BODY_COMPONENT_USER_INPUT'
    REQUEST_BODY_COMPONENT_CONTEXTS = 'REQUEST_BODY_COMPONENT_CONTEXTS'
    REQUEST_BODY_COMPONENT_OUTPUT = 'REQUEST_BODY_COMPONENT_OUTPUT'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of FlaggedSubstringRequestBodyComponent from a JSON string"""
        return cls(json.loads(json_str))


