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


class DigestConfigDigestFrequency(str, Enum):
    """
    DigestFrequency determines the frequency under which digest notifications will be sent.   - DIGEST_FREQUENCY_DAILY: Daily is the frequency for sending digest notifications every day.
    """

    """
    allowed enum values
    """
    DIGEST_FREQUENCY_DAILY = 'DIGEST_FREQUENCY_DAILY'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of DigestConfigDigestFrequency from a JSON string"""
        return cls(json.loads(json_str))


