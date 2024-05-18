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

from ri.apiclient.models.testrunresult_list_test_cases_response import TestrunresultListTestCasesResponse

class TestTestrunresultListTestCasesResponse(unittest.TestCase):
    """TestrunresultListTestCasesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TestrunresultListTestCasesResponse:
        """Test TestrunresultListTestCasesResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TestrunresultListTestCasesResponse`
        """
        model = TestrunresultListTestCasesResponse()
        if include_optional:
            return TestrunresultListTestCasesResponse(
                test_cases = [
                    ri.apiclient.models.testrunresult_test_case.testrunresultTestCase(
                        test_run_id = '', 
                        features = [
                            ''
                            ], 
                        test_batch_type = '', 
                        status = 'TEST_CASE_STATUS_PASS_UNSPECIFIED', 
                        severity = 'SEVERITY_UNSPECIFIED', 
                        importance_score = 1.337, 
                        test_category = 'TEST_CATEGORY_TYPE_UNSPECIFIED', 
                        category = '', 
                        metrics = [
                            ri.apiclient.models.rime_test_metric.rimeTestMetric(
                                metric = '', 
                                category = 'TEST_METRIC_CATEGORY_UNSPECIFIED', 
                                int_value = '', 
                                float_value = 1.337, 
                                empty = ri.apiclient.models.empty.empty(), 
                                str_value = '', 
                                int_list = ri.apiclient.models.rime_int_list.rimeIntList(
                                    values = [
                                        ''
                                        ], ), 
                                float_list = ri.apiclient.models.rime_float_list.rimeFloatList(), 
                                str_list = ri.apiclient.models.rime_str_list.rimeStrList(), 
                                test_case_monitor_info = ri.apiclient.models.test_case_monitor_info_identifies_a_test_metric_as_a_default_monitor.TestCaseMonitorInfo identifies a TestMetric as a default monitor(
                                    threshold = ri.apiclient.models.thresholds_defined_for_the_monitor.Thresholds defined for the Monitor(
                                        low = 1.337, 
                                        high = 1.337, 
                                        type = 'TYPE_UNSPECIFIED', ), 
                                    is_subset_metric = True, 
                                    excluded_transforms = ri.apiclient.models.monitor_excluded_transforms.monitorExcludedTransforms(), ), )
                            ], 
                        url_safe_feature_id = '', 
                        test_case_id = '', 
                        display = ri.apiclient.models.testrunresult_test_case_display.testrunresultTestCaseDisplay(
                            table_info = 'YQ==', 
                            details = 'YQ==', 
                            details_layout = [
                                ''
                                ], ), )
                    ],
                next_page_token = '',
                has_more = True
            )
        else:
            return TestrunresultListTestCasesResponse(
        )
        """

    def testTestrunresultListTestCasesResponse(self):
        """Test TestrunresultListTestCasesResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()