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

from ri.apiclient.models.rime_get_validate_predictions_task_status_response import RimeGetValidatePredictionsTaskStatusResponse

class TestRimeGetValidatePredictionsTaskStatusResponse(unittest.TestCase):
    """RimeGetValidatePredictionsTaskStatusResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RimeGetValidatePredictionsTaskStatusResponse:
        """Test RimeGetValidatePredictionsTaskStatusResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RimeGetValidatePredictionsTaskStatusResponse`
        """
        model = RimeGetValidatePredictionsTaskStatusResponse()
        if include_optional:
            return RimeGetValidatePredictionsTaskStatusResponse(
                resp = ri.apiclient.models.validation_validate_predictions_response.validationValidatePredictionsResponse(
                    is_valid = True, 
                    error_message = '', 
                    validation_status = 'VALIDITY_STATUS_UNSPECIFIED', ),
                job_metadata = ri.apiclient.models.rime_job_metadata.rimeJobMetadata(
                    job_id = '', 
                    job_type = 'JOB_TYPE_UNSPECIFIED', 
                    status = 'JOB_STATUS_UNSPECIFIED', 
                    start_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    creation_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    completion_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    running_time_secs = 1.337, 
                    job_data = ri.apiclient.models.rime_job_data.rimeJobData(
                        stress = ri.apiclient.models.job_data_stress_test.JobDataStressTest(
                            project_id = ri.apiclient.models.rime_uuid.rimeUUID(
                                uuid = '', ), 
                            test_run_id = '', 
                            progress = ri.apiclient.models.rime_stress_test_job_progress.rimeStressTestJobProgress(
                                test_run = ri.apiclient.models.rime_test_run_progress.rimeTestRunProgress(
                                    test_run_id = '', 
                                    test_batches = [
                                        ri.apiclient.models.test_run_progress_test_batch_progress.TestRunProgressTestBatchProgress(
                                            type = '', )
                                        ], ), ), ), 
                        continuous_inc = ri.apiclient.models.job_data_continuous_incremental_test.JobDataContinuousIncrementalTest(
                            firewall_id = '', 
                            ct_test_run_ids = [
                                ''
                                ], ), 
                        file_scan = ri.apiclient.models.job_data_scan.JobDataScan(
                            file_scan_id = '', ), 
                        cross_plane_res = ri.apiclient.models.crossplanetask_cross_plane_response.crossplanetaskCrossPlaneResponse(
                            category_config_generation_service_response = ri.apiclient.models.config_generation_category_config_generation_service_response.config_generationCategoryConfigGenerationServiceResponse(
                                stress_test_categories = [
                                    'TEST_CATEGORY_TYPE_UNSPECIFIED'
                                    ], 
                                continuous_test_categories = [
                                    'TEST_CATEGORY_TYPE_UNSPECIFIED'
                                    ], ), 
                            profiling_config_generation_service_response = ri.apiclient.models.config_generation_profiling_config_generation_service_response.config_generationProfilingConfigGenerationServiceResponse(
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
                                            ], ), ), ), 
                            test_suite_config_generation_service_response = ri.apiclient.models.config_generation_test_suite_config_generation_service_response.config_generationTestSuiteConfigGenerationServiceResponse(
                                test_suite_config = ri.apiclient.models.testrun_test_suite_config.testrunTestSuiteConfig(
                                    global_test_sensitivity = 'TEST_SENSITIVITY_UNSPECIFIED', 
                                    individual_tests_config = '', 
                                    custom_tests = [
                                        ''
                                        ], 
                                    global_exclude_columns = [
                                        ''
                                        ], ), ), 
                            check_object_exists_response = ri.apiclient.models.fileserver_check_object_exists_response.fileserverCheckObjectExistsResponse(
                                exists = True, ), 
                            delete_object_response = ri.apiclient.models.delete_object_response.deleteObjectResponse(), 
                            get_read_object_presigned_link_response = ri.apiclient.models.fileserver_get_read_object_presigned_link_response.fileserverGetReadObjectPresignedLinkResponse(
                                url = '', ), 
                            get_upload_object_presigned_link_response = ri.apiclient.models.fileserver_get_upload_object_presigned_link_response.fileserverGetUploadObjectPresignedLinkResponse(
                                url = '', ), 
                            list_objects_response = ri.apiclient.models.fileserver_list_objects_response.fileserverListObjectsResponse(
                                paths = [
                                    ''
                                    ], ), 
                            validate_dataset_response = ri.apiclient.models.validation_validate_dataset_response.validationValidateDatasetResponse(
                                is_valid = True, 
                                error_message = '', 
                                validation_status = 'VALIDITY_STATUS_UNSPECIFIED', 
                                size_bytes = '', ), 
                            validate_model_response = ri.apiclient.models.validation_validate_model_response.validationValidateModelResponse(
                                is_valid = True, 
                                error_message = '', ), 
                            validate_predictions_response = ri.apiclient.models.validation_validate_predictions_response.validationValidatePredictionsResponse(
                                is_valid = True, 
                                error_message = '', ), ), 
                        generative_model = ri.apiclient.models.rime_job_data_generative_model_test.rimeJobDataGenerativeModelTest(
                            workspace_id = ri.apiclient.models.rime_uuid.rimeUUID(
                                uuid = '', ), 
                            name = '', 
                            url = '', ), ), 
                    job_progress_str = '', 
                    cancellation_requested = True, 
                    agent_id = , 
                    archived_job_logs = ri.apiclient.models.statedb_archived_job_logs.statedbArchivedJobLogs(
                        url = ri.apiclient.models.rime_safe_url.rimeSafeURL(), 
                        expiration_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                    error_msg = '', )
            )
        else:
            return RimeGetValidatePredictionsTaskStatusResponse(
        )
        """

    def testRimeGetValidatePredictionsTaskStatusResponse(self):
        """Test RimeGetValidatePredictionsTaskStatusResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()