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

from ri.apiclient.models.testrunresult_test_feature_result import TestrunresultTestFeatureResult

class TestTestrunresultTestFeatureResult(unittest.TestCase):
    """TestrunresultTestFeatureResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TestrunresultTestFeatureResult:
        """Test TestrunresultTestFeatureResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TestrunresultTestFeatureResult`
        """
        model = TestrunresultTestFeatureResult()
        if include_optional:
            return TestrunresultTestFeatureResult(
                url_safe_feature_id = '',
                feature_name = '',
                feature_type = 'FEATURE_TYPE_UNSPECIFIED',
                severity = 'SEVERITY_UNSPECIFIED',
                summary_counts = ri.apiclient.models.testrunresult_result_summary_counts.testrunresultResultSummaryCounts(
                    total = '', 
                    pass = '', 
                    warning = '', 
                    fail = '', 
                    skip = '', ),
                failing_tests = [
                    ''
                    ],
                num_failing_rows = '',
                failing_rows_html = '',
                drift_statistic = ri.apiclient.models.rime_named_double.rimeNamedDouble(
                    name = '', 
                    value = 1.337, ),
                model_impact = ri.apiclient.models.rime_named_double.rimeNamedDouble(
                    name = '', 
                    value = 1.337, ),
                feature_infos = [
                    ''
                    ],
                display = ri.apiclient.models.testrunresult_test_feature_result_display.testrunresultTestFeatureResultDisplay(
                    summary_details = 'YQ==', 
                    table_columns_to_show = [
                        ri.apiclient.models.rime_table_column.rimeTableColumn(
                            name = '', 
                            description = '', 
                            type = 'TABLE_COLUMN_TYPE_UNSPECIFIED', )
                        ], )
            )
        else:
            return TestrunresultTestFeatureResult(
        )
        """

    def testTestrunresultTestFeatureResult(self):
        """Test TestrunresultTestFeatureResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()