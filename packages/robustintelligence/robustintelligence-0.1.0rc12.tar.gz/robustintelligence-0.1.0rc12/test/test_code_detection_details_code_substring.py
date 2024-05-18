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

from ri.apiclient.models.code_detection_details_code_substring import CodeDetectionDetailsCodeSubstring

class TestCodeDetectionDetailsCodeSubstring(unittest.TestCase):
    """CodeDetectionDetailsCodeSubstring unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CodeDetectionDetailsCodeSubstring:
        """Test CodeDetectionDetailsCodeSubstring
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CodeDetectionDetailsCodeSubstring`
        """
        model = CodeDetectionDetailsCodeSubstring()
        if include_optional:
            return CodeDetectionDetailsCodeSubstring(
                language = '',
                flagged_substring = ri.apiclient.models.generativefirewall_flagged_substring.generativefirewallFlaggedSubstring(
                    request_body_component = 'REQUEST_BODY_COMPONENT_UNSPECIFIED', 
                    context_index = '', 
                    substring_start_index = '', 
                    substring_end_index = '', )
            )
        else:
            return CodeDetectionDetailsCodeSubstring(
        )
        """

    def testCodeDetectionDetailsCodeSubstring(self):
        """Test CodeDetectionDetailsCodeSubstring"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()