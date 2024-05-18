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

from ri.apiclient.models.model_testing_start_continuous_test_request import ModelTestingStartContinuousTestRequest

class TestModelTestingStartContinuousTestRequest(unittest.TestCase):
    """ModelTestingStartContinuousTestRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ModelTestingStartContinuousTestRequest:
        """Test ModelTestingStartContinuousTestRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ModelTestingStartContinuousTestRequest`
        """
        model = ModelTestingStartContinuousTestRequest()
        if include_optional:
            return ModelTestingStartContinuousTestRequest(
                firewall_id = ri.apiclient.models.uniquely_specifies_a_firewall/.Uniquely specifies a Firewall.(),
                test_run_incremental_config = ri.apiclient.models.testrun_test_run_incremental_config.testrunTestRunIncrementalConfig(
                    eval_dataset_id = '', 
                    run_time_info = ri.apiclient.models.runtimeinfo_run_time_info.runtimeinfoRunTimeInfo(
                        custom_image = ri.apiclient.models.runtimeinfo_custom_image_type.runtimeinfoCustomImageType(
                            managed_image_name = '', ), 
                        resource_request = ri.apiclient.models.runtimeinfo_resource_request.runtimeinfoResourceRequest(
                            ram_request_megabytes = '', 
                            cpu_request_millicores = '', ), 
                        explicit_errors = True, 
                        random_seed = '', ), ),
                override_existing_bins = True,
                agent_id = ri.apiclient.models.rime_uuid.rimeUUID(
                    uuid = '', ),
                experimental_fields = {
                    'key' : None
                    }
            )
        else:
            return ModelTestingStartContinuousTestRequest(
        )
        """

    def testModelTestingStartContinuousTestRequest(self):
        """Test ModelTestingStartContinuousTestRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()