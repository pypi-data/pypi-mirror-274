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

from ri.apiclient.models.rime_list_enabled_features_response import RimeListEnabledFeaturesResponse

class TestRimeListEnabledFeaturesResponse(unittest.TestCase):
    """RimeListEnabledFeaturesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RimeListEnabledFeaturesResponse:
        """Test RimeListEnabledFeaturesResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RimeListEnabledFeaturesResponse`
        """
        model = RimeListEnabledFeaturesResponse()
        if include_optional:
            return RimeListEnabledFeaturesResponse(
                customer_name = '',
                enabled_features = [
                    'LICENSE_FEATURE_UNSPECIFIED'
                    ]
            )
        else:
            return RimeListEnabledFeaturesResponse(
        )
        """

    def testRimeListEnabledFeaturesResponse(self):
        """Test RimeListEnabledFeaturesResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()