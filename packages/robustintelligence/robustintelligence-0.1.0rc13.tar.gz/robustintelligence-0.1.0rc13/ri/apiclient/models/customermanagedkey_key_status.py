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


class CustomermanagedkeyKeyStatus(str, Enum):
    """
    KeyStatus specifies the status of a customer managed key.   - KEY_STATUS_ACTIVE: The key is enabled and is used for encryption and decryption.  - KEY_STATUS_REVOKED: The key is disabled and cannot be used for encryption and decryption. The RI platform has no access to customer data if the key is disabled.
    """

    """
    allowed enum values
    """
    KEY_STATUS_ACTIVE = 'KEY_STATUS_ACTIVE'
    KEY_STATUS_REVOKED = 'KEY_STATUS_REVOKED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of CustomermanagedkeyKeyStatus from a JSON string"""
        return cls(json.loads(json_str))


