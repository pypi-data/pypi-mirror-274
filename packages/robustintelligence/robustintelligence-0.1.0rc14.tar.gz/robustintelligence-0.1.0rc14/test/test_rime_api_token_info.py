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

from ri.apiclient.models.rime_api_token_info import RimeAPITokenInfo

class TestRimeAPITokenInfo(unittest.TestCase):
    """RimeAPITokenInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RimeAPITokenInfo:
        """Test RimeAPITokenInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RimeAPITokenInfo`
        """
        model = RimeAPITokenInfo()
        if include_optional:
            return RimeAPITokenInfo(
                id = ri.apiclient.models.rime_uuid.rimeUUID(
                    uuid = '', ),
                name = '',
                suffix = '',
                creation_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                expiration_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                workspace_id = ri.apiclient.models.rime_uuid.rimeUUID(
                    uuid = '', ),
                user_id = '',
                token_type = 'TOKEN_TYPE_UNSPECIFIED'
            )
        else:
            return RimeAPITokenInfo(
        )
        """

    def testRimeAPITokenInfo(self):
        """Test RimeAPITokenInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()