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

from ri.apiclient.models.project_project_with_details import ProjectProjectWithDetails

class TestProjectProjectWithDetails(unittest.TestCase):
    """ProjectProjectWithDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ProjectProjectWithDetails:
        """Test ProjectProjectWithDetails
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ProjectProjectWithDetails`
        """
        model = ProjectProjectWithDetails()
        if include_optional:
            return ProjectProjectWithDetails(
                project = ri.apiclient.models.project_project.projectProject(
                    id = ri.apiclient.models.rime_uuid.rimeUUID(
                        uuid = '', ), 
                    name = '', 
                    description = '', 
                    use_case = '', 
                    ethical_consideration = '', 
                    creation_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    owner_id = ri.apiclient.models.rime_uuid.rimeUUID(
                        uuid = '', ), 
                    workspace_id = , 
                    model_task = 'MODEL_TASK_UNSPECIFIED', 
                    tags = [
                        ''
                        ], 
                    firewall_ids = [
                        
                        ], 
                    project_test_suite_config = ri.apiclient.models.testrun_test_suite_config.testrunTestSuiteConfig(
                        global_test_sensitivity = 'TEST_SENSITIVITY_UNSPECIFIED', 
                        individual_tests_config = '', 
                        custom_tests = [
                            ''
                            ], 
                        global_exclude_columns = [
                            ''
                            ], ), 
                    profiling_config = ri.apiclient.models.testrun_profiling_config.testrunProfilingConfig(
                        data_profiling = ri.apiclient.models.testrun_data_profiling.testrunDataProfiling(
                            num_quantiles = '', 
                            num_subsets = '', 
                            column_type_info = ri.apiclient.models.data_profiling_column_type_info.DataProfilingColumnTypeInfo(
                                min_nunique_for_numeric = '', 
                                numeric_violation_threshold = 1.337, 
                                categorical_violation_threshold = 1.337, 
                                min_unique_prop = 1.337, 
                                allow_float_unique = True, 
                                numeric_range_inference_threshold = 1.337, 
                                unseen_values_allowed_criteria = 1.337, ), 
                            feature_relationship_info = ri.apiclient.models.data_profiling_feature_relationship_info.DataProfilingFeatureRelationshipInfo(
                                num_feats_to_profile = '', 
                                compute_feature_relationships = True, 
                                compute_numeric_feature_relationships = True, 
                                ignore_nan_for_feature_relationships = True, ), ), 
                        model_profiling = ri.apiclient.models.testrun_model_profiling.testrunModelProfiling(
                            nrows_for_summary = '', 
                            nrows_for_feature_importance = '', 
                            metric_configs_json = '', 
                            impact_metric = '', 
                            impact_label_threshold = 1.337, 
                            drift_impact_metric = '', 
                            subset_summary_metric = '', 
                            num_feats_for_subset_summary = '', 
                            custom_metrics = [
                                ri.apiclient.models.testrun_custom_metric.testrunCustomMetric(
                                    name = '', 
                                    file_path = '', 
                                    range_lower_bound = 1.337, 
                                    range_upper_bound = 1.337, 
                                    run_subset_performance = True, 
                                    run_subset_performance_drift = True, 
                                    run_overall_performance = True, 
                                    metadata = ri.apiclient.models.custom_metric_custom_metric_metadata.CustomMetricCustomMetricMetadata(
                                        short_description = '', 
                                        starter_description = '', 
                                        why_it_matters_description = '', 
                                        configuration_description = '', 
                                        example_description = '', ), )
                                ], ), ), 
                    run_time_info = ri.apiclient.models.runtimeinfo_run_time_info.runtimeinfoRunTimeInfo(
                        custom_image = ri.apiclient.models.runtimeinfo_custom_image_type.runtimeinfoCustomImageType(
                            managed_image_name = '', ), 
                        resource_request = ri.apiclient.models.runtimeinfo_resource_request.runtimeinfoResourceRequest(
                            ram_request_megabytes = '', 
                            cpu_request_millicores = '', ), 
                        explicit_errors = True, 
                        random_seed = '', ), 
                    is_published = True, 
                    last_test_run_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    stress_test_categories = [
                        'TEST_CATEGORY_TYPE_UNSPECIFIED'
                        ], 
                    continuous_test_categories = [
                        'TEST_CATEGORY_TYPE_UNSPECIFIED'
                        ], 
                    risk_scores = [
                        ri.apiclient.models.riskscore_risk_score.riskscoreRiskScore(
                            type = 'RISK_CATEGORY_TYPE_UNSPECIFIED', 
                            severity = 'SEVERITY_UNSPECIFIED', 
                            score = 1.337, )
                        ], 
                    active_schedule = ri.apiclient.models.project_schedule_info.projectScheduleInfo(
                        schedule_id = , 
                        activated_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), ),
                owner_details = ri.apiclient.models.owner_details_returns_a_limited_details_about_a_user
to_provide_identity_of_the_owner_of_the_project.OwnerDetails returns a limited details about a user
to provide identity of the owner of the Project(
                    name = '', 
                    email = '', ),
                last_updated_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return ProjectProjectWithDetails(
        )
        """

    def testProjectProjectWithDetails(self):
        """Test ProjectProjectWithDetails"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()