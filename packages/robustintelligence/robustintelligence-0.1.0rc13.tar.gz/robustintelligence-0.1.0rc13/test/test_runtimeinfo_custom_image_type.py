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

from ri.apiclient.models.runtimeinfo_custom_image_type import RuntimeinfoCustomImageType

class TestRuntimeinfoCustomImageType(unittest.TestCase):
    """RuntimeinfoCustomImageType unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RuntimeinfoCustomImageType:
        """Test RuntimeinfoCustomImageType
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RuntimeinfoCustomImageType`
        """
        model = RuntimeinfoCustomImageType()
        if include_optional:
            return RuntimeinfoCustomImageType(
                custom_image = ri.apiclient.models.runtimeinfo_custom_image.runtimeinfoCustomImage(
                    name = '', 
                    pull_secret = ri.apiclient.models.custom_image_pull_secret.CustomImagePullSecret(
                        name = '', ), ),
                managed_image_name = ''
            )
        else:
            return RuntimeinfoCustomImageType(
        )
        """

    def testRuntimeinfoCustomImageType(self):
        """Test RuntimeinfoCustomImageType"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()