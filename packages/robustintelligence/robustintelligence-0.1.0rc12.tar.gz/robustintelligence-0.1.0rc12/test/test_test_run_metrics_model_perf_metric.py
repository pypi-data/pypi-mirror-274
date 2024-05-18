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

from ri.apiclient.models.test_run_metrics_model_perf_metric import TestRunMetricsModelPerfMetric

class TestTestRunMetricsModelPerfMetric(unittest.TestCase):
    """TestRunMetricsModelPerfMetric unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TestRunMetricsModelPerfMetric:
        """Test TestRunMetricsModelPerfMetric
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TestRunMetricsModelPerfMetric`
        """
        model = TestRunMetricsModelPerfMetric()
        if include_optional:
            return TestRunMetricsModelPerfMetric(
                ref_metric = 1.337,
                eval_metric = 1.337
            )
        else:
            return TestRunMetricsModelPerfMetric(
        )
        """

    def testTestRunMetricsModelPerfMetric(self):
        """Test TestRunMetricsModelPerfMetric"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()