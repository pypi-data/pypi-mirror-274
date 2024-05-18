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


class GenerativetestingObjectiveSubCategory(str, Enum):
    """
    ObjectiveSubCategory is the specific intent that the attack prompt is trying to achieve.
    """

    """
    allowed enum values
    """
    OBJECTIVE_SUB_CATEGORY_THEFT = 'OBJECTIVE_SUB_CATEGORY_THEFT'
    OBJECTIVE_SUB_CATEGORY_POISONING = 'OBJECTIVE_SUB_CATEGORY_POISONING'
    OBJECTIVE_SUB_CATEGORY_VIOLENCE = 'OBJECTIVE_SUB_CATEGORY_VIOLENCE'
    OBJECTIVE_SUB_CATEGORY_STALKING = 'OBJECTIVE_SUB_CATEGORY_STALKING'
    OBJECTIVE_SUB_CATEGORY_TERRORISM = 'OBJECTIVE_SUB_CATEGORY_TERRORISM'
    OBJECTIVE_SUB_CATEGORY_BOMB = 'OBJECTIVE_SUB_CATEGORY_BOMB'
    OBJECTIVE_SUB_CATEGORY_MURDER = 'OBJECTIVE_SUB_CATEGORY_MURDER'
    OBJECTIVE_SUB_CATEGORY_PII_SSN = 'OBJECTIVE_SUB_CATEGORY_PII_SSN'
    OBJECTIVE_SUB_CATEGORY_PII_PHONE_NUMBER = 'OBJECTIVE_SUB_CATEGORY_PII_PHONE_NUMBER'
    OBJECTIVE_SUB_CATEGORY_PII_CREDIT_CARD = 'OBJECTIVE_SUB_CATEGORY_PII_CREDIT_CARD'
    OBJECTIVE_SUB_CATEGORY_PII_EMAIL_ADDRESS = 'OBJECTIVE_SUB_CATEGORY_PII_EMAIL_ADDRESS'
    OBJECTIVE_SUB_CATEGORY_PII_PASSPORT_NUMBER = 'OBJECTIVE_SUB_CATEGORY_PII_PASSPORT_NUMBER'
    OBJECTIVE_SUB_CATEGORY_PIRACY = 'OBJECTIVE_SUB_CATEGORY_PIRACY'
    OBJECTIVE_SUB_CATEGORY_HACKING = 'OBJECTIVE_SUB_CATEGORY_HACKING'
    OBJECTIVE_SUB_CATEGORY_VIRUS = 'OBJECTIVE_SUB_CATEGORY_VIRUS'
    OBJECTIVE_SUB_CATEGORY_MISINFORMATION = 'OBJECTIVE_SUB_CATEGORY_MISINFORMATION'
    OBJECTIVE_SUB_CATEGORY_FINANCIAL_ADVICE = 'OBJECTIVE_SUB_CATEGORY_FINANCIAL_ADVICE'
    OBJECTIVE_SUB_CATEGORY_PII = 'OBJECTIVE_SUB_CATEGORY_PII'
    OBJECTIVE_SUB_CATEGORY_PROMPT_EXTRACTION = 'OBJECTIVE_SUB_CATEGORY_PROMPT_EXTRACTION'
    OBJECTIVE_SUB_CATEGORY_FINANCIAL = 'OBJECTIVE_SUB_CATEGORY_FINANCIAL'
    OBJECTIVE_SUB_CATEGORY_COPYRIGHT_EXTRACTION = 'OBJECTIVE_SUB_CATEGORY_COPYRIGHT_EXTRACTION'
    OBJECTIVE_SUB_CATEGORY_LONG_PROMPTS = 'OBJECTIVE_SUB_CATEGORY_LONG_PROMPTS'
    OBJECTIVE_SUB_CATEGORY_CHILD_PORN = 'OBJECTIVE_SUB_CATEGORY_CHILD_PORN'
    OBJECTIVE_SUB_CATEGORY_DRUGS = 'OBJECTIVE_SUB_CATEGORY_DRUGS'
    OBJECTIVE_SUB_CATEGORY_SUICIDE = 'OBJECTIVE_SUB_CATEGORY_SUICIDE'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of GenerativetestingObjectiveSubCategory from a JSON string"""
        return cls(json.loads(json_str))


