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

from ri.apiclient.models.generativefirewall_update_firewall_instance_response import GenerativefirewallUpdateFirewallInstanceResponse

class TestGenerativefirewallUpdateFirewallInstanceResponse(unittest.TestCase):
    """GenerativefirewallUpdateFirewallInstanceResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GenerativefirewallUpdateFirewallInstanceResponse:
        """Test GenerativefirewallUpdateFirewallInstanceResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GenerativefirewallUpdateFirewallInstanceResponse`
        """
        model = GenerativefirewallUpdateFirewallInstanceResponse()
        if include_optional:
            return GenerativefirewallUpdateFirewallInstanceResponse(
                updated_firewall_instance = ri.apiclient.models.generativefirewall_firewall_instance_info.generativefirewallFirewallInstanceInfo(
                    firewall_instance_id = ri.apiclient.models.rime_uuid.rimeUUID(
                        uuid = '', ), 
                    config = ri.apiclient.models.generativefirewall_firewall_rule_config.generativefirewallFirewallRuleConfig(
                        language = 'LANGUAGE_UNSPECIFIED', 
                        selected_rules = [
                            'FIREWALL_RULE_TYPE_UNSPECIFIED'
                            ], 
                        individual_rules_config = ri.apiclient.models.generativefirewall_individual_rules_config.generativefirewallIndividualRulesConfig(
                            off_topic = ri.apiclient.models.generativefirewall_off_topic_rule_config.generativefirewallOffTopicRuleConfig(
                                in_domain_intents = [
                                    ''
                                    ], 
                                restricted_intents = [
                                    ''
                                    ], 
                                in_domain_intents_sensitivity = 'RULE_SENSITIVITY_UNSPECIFIED', 
                                restricted_intents_sensitivity = 'RULE_SENSITIVITY_UNSPECIFIED', ), 
                            pii_detection_input = ri.apiclient.models.generativefirewall_pii_detection_rule_config.generativefirewallPiiDetectionRuleConfig(
                                entity_types = [
                                    'PII_ENTITY_TYPE_UNSPECIFIED'
                                    ], 
                                custom_entities = [
                                    ri.apiclient.models.generativefirewall_custom_pii_entity.generativefirewallCustomPiiEntity(
                                        name = '', 
                                        patterns = [
                                            ''
                                            ], 
                                        context_words = [
                                            ''
                                            ], )
                                    ], ), 
                            pii_detection_output = ri.apiclient.models.generativefirewall_pii_detection_rule_config.generativefirewallPiiDetectionRuleConfig(), 
                            token_counter_input = ri.apiclient.models.generativefirewall_token_counter_rule_config.generativefirewallTokenCounterRuleConfig(
                                firewall_tokenizer = 'FIREWALL_TOKENIZER_UNSPECIFIED', 
                                max_tokens = '', ), 
                            token_counter_output = ri.apiclient.models.generativefirewall_token_counter_rule_config.generativefirewallTokenCounterRuleConfig(
                                max_tokens = '', ), 
                            unknown_external_source = ri.apiclient.models.generativefirewall_unknown_external_source_rule_config.generativefirewallUnknownExternalSourceRuleConfig(
                                whitelisted_urls = [
                                    ''
                                    ], 
                                ignore_contexts = True, ), 
                            language_detection = ri.apiclient.models.generativefirewall_language_detection_rule_config.generativefirewallLanguageDetectionRuleConfig(
                                whitelisted_languages = [
                                    'LANGUAGE_UNSPECIFIED'
                                    ], ), 
                            prompt_injection = ri.apiclient.models.generativefirewall_prompt_injection_rule_config.generativefirewallPromptInjectionRuleConfig(
                                prompt_injection_rule_sensitivity = 'RULE_SENSITIVITY_UNSPECIFIED', ), 
                            toxicity_rule_config_input = ri.apiclient.models.generativefirewall_toxicity_rule_config.generativefirewallToxicityRuleConfig(
                                toxicity_rule_sensitivity = 'RULE_SENSITIVITY_UNSPECIFIED', ), 
                            toxicity_rule_config_output = ri.apiclient.models.generativefirewall_toxicity_rule_config.generativefirewallToxicityRuleConfig(), 
                            code_detection = ri.apiclient.models.generativefirewall_code_detection_rule_config.generativefirewallCodeDetectionRuleConfig(
                                malicious = True, 
                                ignore_contexts = True, ), ), ), 
                    deployment_status = 'FIREWALL_INSTANCE_STATUS_UNSPECIFIED', 
                    description = '', 
                    agent_id = ri.apiclient.models.rime_uuid.rimeUUID(
                        uuid = '', ), 
                    spec = ri.apiclient.models.generativefirewall_firewall_instance_deployment_config.generativefirewallFirewallInstanceDeploymentConfig(
                        pod_annotations = {
                            'key' : ''
                            }, ), 
                    last_heartbeat_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return GenerativefirewallUpdateFirewallInstanceResponse(
        )
        """

    def testGenerativefirewallUpdateFirewallInstanceResponse(self):
        """Test GenerativefirewallUpdateFirewallInstanceResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()