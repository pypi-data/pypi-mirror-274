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

from ri.apiclient.models.rime_create_notification_request import RimeCreateNotificationRequest

class TestRimeCreateNotificationRequest(unittest.TestCase):
    """RimeCreateNotificationRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RimeCreateNotificationRequest:
        """Test RimeCreateNotificationRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RimeCreateNotificationRequest`
        """
        model = RimeCreateNotificationRequest()
        if include_optional:
            return RimeCreateNotificationRequest(
                object_type = 'OBJECT_TYPE_UNSPECIFIED',
                object_id = '',
                emails = [
                    ''
                    ],
                config = ri.apiclient.models.schemanotification_config.schemanotificationConfig(
                    digest_config = ri.apiclient.models.notification_digest_config.notificationDigestConfig(
                        frequency = 'DIGEST_FREQUENCY_UNSPECIFIED', 
                        hour_offset = 56, 
                        last_digest_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                    job_action_config = ri.apiclient.models.notification_job_action_config.notificationJobActionConfig(), 
                    monitoring_config = ri.apiclient.models.notification_monitoring_config.notificationMonitoringConfig(
                        level = 'ALERT_LEVEL_UNSPECIFIED', ), ),
                webhooks = [
                    ri.apiclient.models.notification_webhook_config.notificationWebhookConfig(
                        webhook = '', )
                    ]
            )
        else:
            return RimeCreateNotificationRequest(
                object_id = '',
        )
        """

    def testRimeCreateNotificationRequest(self):
        """Test RimeCreateNotificationRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()