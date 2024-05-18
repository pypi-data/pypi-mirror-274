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
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ValidateRequest(BaseModel):
    """
    ValidateRequest is a single request to the firewall on a piece of user input / output. Either the input or output must be provided.
    """ # noqa: E501
    user_input_text: Optional[StrictStr] = Field(default=None, description="Input text is the raw user input. The generative firewall performs validation on input to prevent risk configured by firewall rules.", alias="userInputText")
    contexts: Optional[List[StrictStr]] = Field(default=None, description="Documents that represent relevant context for the input query that is fed into the model. e.g. in a RAG application this will be the documents loaded during the RAG Retrieval phase to augment the LLM's response.")
    output_text: Optional[StrictStr] = Field(default=None, description="Output text is the raw output text of the model. The generative firewall performs validation on the output so the system can determine whether to show it to users.", alias="outputText")
    firewall_instance_id: Optional[Dict[str, Any]] = Field(default=None, description="Unique ID of an object in RIME.", alias="firewallInstanceId")
    __properties: ClassVar[List[str]] = ["userInputText", "contexts", "outputText", "firewallInstanceId"]

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
        """Create an instance of ValidateRequest from a JSON string"""
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
        """Create an instance of ValidateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "userInputText": obj.get("userInputText"),
            "contexts": obj.get("contexts"),
            "outputText": obj.get("outputText"),
            "firewallInstanceId": obj.get("firewallInstanceId")
        })
        return _obj


