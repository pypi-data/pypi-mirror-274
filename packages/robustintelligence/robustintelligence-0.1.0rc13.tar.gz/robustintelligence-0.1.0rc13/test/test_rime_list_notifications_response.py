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

from ri.apiclient.models.rime_list_notifications_response import RimeListNotificationsResponse

class TestRimeListNotificationsResponse(unittest.TestCase):
    """RimeListNotificationsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RimeListNotificationsResponse:
        """Test RimeListNotificationsResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RimeListNotificationsResponse`
        """
        model = RimeListNotificationsResponse()
        if include_optional:
            return RimeListNotificationsResponse(
                notifications = [
                    ri.apiclient.models.notification_notification.notificationNotification(
                        id = ri.apiclient.models.rime_uuid.rimeUUID(
                            uuid = '', ), 
                        object_type = 'OBJECT_TYPE_UNSPECIFIED', 
                        object_id = '', 
                        notification_type = 'NOTIFICATION_TYPE_UNSPECIFIED', 
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
                            ], 
                        emails = [
                            ''
                            ], 
                        last_send_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ],
                next_page_token = '',
                has_more = True
            )
        else:
            return RimeListNotificationsResponse(
        )
        """

    def testRimeListNotificationsResponse(self):
        """Test RimeListNotificationsResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()