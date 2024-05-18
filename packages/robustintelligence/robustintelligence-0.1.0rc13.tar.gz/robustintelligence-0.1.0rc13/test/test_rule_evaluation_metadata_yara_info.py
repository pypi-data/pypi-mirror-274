# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import unittest

from ri.apiclient.models.rule_evaluation_metadata_yara_info import RuleEvaluationMetadataYaraInfo

class TestRuleEvaluationMetadataYaraInfo(unittest.TestCase):
    """RuleEvaluationMetadataYaraInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RuleEvaluationMetadataYaraInfo:
        """Test RuleEvaluationMetadataYaraInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RuleEvaluationMetadataYaraInfo`
        """
        model = RuleEvaluationMetadataYaraInfo()
        if include_optional:
            return RuleEvaluationMetadataYaraInfo(
                is_decisive_match = True,
                action = 'FIREWALL_ACTION_UNSPECIFIED',
                matched_by_rules = [
                    ''
                    ]
            )
        else:
            return RuleEvaluationMetadataYaraInfo(
        )
        """

    def testRuleEvaluationMetadataYaraInfo(self):
        """Test RuleEvaluationMetadataYaraInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()