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


class RimeAgentStatus(str, Enum):
    """
    The status of the agent.   - AGENT_STATUS_PENDING: Resources have been created for the agent but the agent has not started yet.  - AGENT_STATUS_ACTIVE: Agent can run jobs.  - AGENT_STATUS_UNRESPONSIVE: No agent heartbeat for three minutes.  - AGENT_STATUS_DEACTIVATED: Agent can no longer run jobs and can be deleted. (Deprecated after Deactivation and Deletion endpoints are combined)
    """

    """
    allowed enum values
    """
    AGENT_STATUS_PENDING = 'AGENT_STATUS_PENDING'
    AGENT_STATUS_ACTIVE = 'AGENT_STATUS_ACTIVE'
    AGENT_STATUS_UNRESPONSIVE = 'AGENT_STATUS_UNRESPONSIVE'
    AGENT_STATUS_DEACTIVATED = 'AGENT_STATUS_DEACTIVATED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RimeAgentStatus from a JSON string"""
        return cls(json.loads(json_str))


