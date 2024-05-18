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

from ri.apiclient.models.detection_event_detail import DetectionEventDetail

class TestDetectionEventDetail(unittest.TestCase):
    """DetectionEventDetail unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DetectionEventDetail:
        """Test DetectionEventDetail
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DetectionEventDetail`
        """
        model = DetectionEventDetail()
        if include_optional:
            return DetectionEventDetail(
                metric_degradation = ri.apiclient.models.detection_metric_degradation_event_details.detectionMetricDegradationEventDetails(),
                security = ri.apiclient.models.detection_security_event_details.detectionSecurityEventDetails(
                    type = 'SECURITY_EVENT_TYPE_UNSPECIFIED', 
                    effect_on_model = [
                        ''
                        ], 
                    possible_intent = [
                        ''
                        ], 
                    evidence = , 
                    recommendations = [
                        ''
                        ], 
                    datapoints = [
                        ri.apiclient.models.security_event_details_flagged_datapoint.SecurityEventDetailsFlaggedDatapoint(
                            row_id = '', 
                            row_timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                        ], )
            )
        else:
            return DetectionEventDetail(
        )
        """

    def testDetectionEventDetail(self):
        """Test DetectionEventDetail"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()