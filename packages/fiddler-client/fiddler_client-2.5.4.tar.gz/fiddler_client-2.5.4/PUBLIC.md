Fiddler Client
=============

Python client for interacting with Fiddler. Provides a user-friendly interface to our REST API and enables event
publishing for use with our monitoring features.

Requirements
------------
Requires Python >= Python-3.6.3 and pip >= 19.0

Installation
------------

    $ pip3 install fiddler-client

API Example Usage
-------------
Documentation for the API can be found [here](https://docs.fiddler.ai/reference/about-the-fiddler-client). For examples of interacting with our APIs, please check out our [Quick Start Guide](https://docs.fiddler.ai/docs/quick-start) as well as the notebooks found on our [Examples Github](https://github.com/fiddler-labs/fiddler-examples).

Version History
-------------
### 2.5.2
  - #### **Modifications**
    - Fix pydantic issue with typing-extensions versions > 4.5.0
### 2.5.1
  - #### **New Features**
    - Support tf_idf vectors in `TextEmbedding` type column definition
### 2.5.0
  - #### **New Features**
    - Add support for enrichments
    - Allow pausing multiple alerts at once
    - Add percentage violation metrics for alert
    - Support for alert revisions

### 2.4.1
  - ### **Modifications**
    - Fix slice query with `vector` type columns

### 2.4.0
  - ### **New Features**
    - Add support for segments
  - #### **Modifications**
    - Ensure `TextEmbedding` and `ImageEmbedding` is supported for vectors in metadata

### 2.3.0
  - #### **New Features**
    - Added support for creating alerts on the `Frequency` metric.
  - #### **Modifications**
    - Relax pydantic version to allow any version between 1.9 and 2

### 2.2.1
  - #### **Modifications**
    - Relax pydantic version to allow any version between 1.9 and 2

### 2.2.0
  - #### **Modifications**
    - `add_custom_metric()` supports an optional `description` parameter
    - `fql` is renamed to `definition` in `add_custom_metric()`
    - A new `get_custom_metric()` function to get details about a single custom metric.

### 2.1.2
  - #### **Modifications**
    - Relax pydantic version to allow any version between 1.9 and 2

### 2.1.1
  - #### **Modifications**
    - Update `pyarrow` requirement to `7.0.0`.

### 2.1.0
 - #### **New Features**
  - Introduce Model Tasks `NOT_SET` and `LLM`
  - Relax Target / Output specification for model tasks `NOT_SET` and `LLM`
  - Support custom metrics
 - #### **Modifications**
  - `DatasetDataSource` and `EventIdDataSource` will take `dataset_id` instead of `dataset_name`
  - `list_baselines()` to return baseline names instead of baseline objects

### 2.0.8
  - #### **Modifications**
    - Relax pydantic version to allow any version between 1.9 and 2

### 2.0.7
  - #### **Modifications**
    - Support string metric types for alert creation, for server 23.7.

### 2.0.6
  - #### **Modifications**
    - Update `pyarrow` requirement to `7.0.0`.

### 2.0.5
  - #### **Modifications**
    - Fix for a minor bug in `fdl.DatasetInfo.from_dataframe()`

### 2.0.4
  - #### **Modifications**
    - Update `pyarrow` requirement to `13.0.0`.

### 2.0.3
  - #### **Modifications**
    - Relax pandas version for 2.0.
    - get_slice() `query` parameter reverted to `sql_query`

### 2.0.2
  - #### **Modifications**
    - Fix Parquet conversion issue in `upload_dataset` and `publish_event_batch`

### 2.0.1
  - #### **Removed**
    - Following methods are removed
      - register_model
      - upload_model_package
      - update_model
      - trigger_pre_computation
      - _trigger_model_predictions
      - generate_sample_events
      - list_teams
      - list_project_roles
      - list_org_roles
      - unshare_project
      - share_project
      - process_avro
      - process_csv
  - #### **New Features**
    - Add `monitor_components` as an attribute for `CustomFeature` of type `FROM_COLUMNS`. Default as `False`
    - Adds new statistic type `SUM` to supported alert metrics
    - Support `CustomFeature` of type `FROM_VECTOR` `FROM_TEXT_EMBEDDING` and `FROM_IMAGE_EMBEDDING`
  - #### **Modificatiosn**
    - Remove `column` as a parameter in `add_alert_rule` and `get_alert_rules` functions
    - Default `FileType` Parquet in `upload_dataset` and `publish_event_batch`
    - - get_slice() `sql_query` parameter changed to `query`

### 1.8.6
 - #### **Modifications**
  - Relax pandas version for 2.0.

### 1.8.4
 - #### **New Features**
  - New DeploymentType enum for `MANUAL` deployment

### 1.8.3
 - #### **Modifications**
  - New `columns` parameter in add_alert_rule and get_alert_rules to support multiple columns to be used for server version >= 23.3.0
  - get_triggered_alerts supports `alert_value` as a float as well as a dict

### 1.8.2
  - #### **Modifications**
    - Fixed a bug where `min` and `max` for columns of type `float` in `dataset_info` are cast into `int` after uploaded

### 1.8.1
  - #### **Modifications**
    - Fixed a bug wherein null string was going in request body if body wasn't specified.
    - Fix `categorical_target_class_details` when passed as an array
    - Fix a bug where `fdl.ModelInputType.TEXT` were not being accepted properly
    - Fix `categorical_target_class_details` when passed as an empty list


### 1.8.0
  - #### **Modifications**
    - Add new alert type -  `statistic` for setting alerts
    - Add `target_class_order` as a required field of `ModelInfo` object when `model_task` is `MULTICLASS_CLASSIFICATION`,
      `RANKING` or `BINARY_CLASSIFICATION`. Only applies for `BINARY_CLASSIFICATION` when target column is of type `CATEGORY`
    - Add `columns` as a parameter in `add_alert_rule` and `get_alert_rules` functions
    - Add deprecation warning for `column` as a parameter in `add_alert_rule` and `get_alert_rules` functions

### 1.7.4
  - #### **Modification**
    - Do not typecast column with strings in get_slice()

### 1.7.3
  - #### **Modification**
    - Send row and column count information to dataset upload api

### 1.7.2
  - #### **Modification**
    - Bring back `WeightingParams` object

### 1.7.1
  - #### **Modification**
    - Relaxed boto3 version constraint

### 1.7.0
  - #### **Removed**
    - Remove support for initializing fiddler client with version=1
    - Following methods are removed
      - get_segment_info
      - delete_segment
      - deactivate_segment
      - activate_segment
      - list_segments
      - upload_segment
      - add_monitoring_config
      - publish_parquet_s3
      - publish_events_log

### 1.6.2
  - #### **Modifications**
    - Make dataset_id a required field in add_model()
    - Update max_inferred_cardinality to 100
  - #### **New Features**
    - New method for updating a model artifact `update_model_artifact`

### 1.5.3
  - #### **Modifications**
    - Fix add_model_artifact error for NLP models
    - Add model_info validation during add_model

### 1.5.2
  - #### **Modifications**
    - Add fix for self signed certificate not working by adding verify param to FiddlerApi

### 1.5.1
  - #### **Modifications**
    - Fix in `violation_of_type` to include numpy dtypes such as `int64`

### 1.5.0
  - #### **New Features**
    - New methods addition for alert rules: `add_alert_rule`, `get_alert_rules`, `delete_alert_rule`
    - New method to get triggered alerts for an alert rule: `get_triggered_alerts`

### 1.4.5
  - #### **Modifications**
    - Assert nullable columns in `missing_value_encodings`(If users send non-nullable columns as `missing_value_encodings`, Fiddler converts them as nullable automatically with a warning)

### 1.4.4
  - #### **Modifications**
    - Allow types other than `Column data_type` for `missing_value_encodings`.

### 1.4.3
  - #### **Modifications**
    - Accept `string` `'inf'` in `float` columns in `missing_value_encodings`.

### 1.4.2
  - #### **New Features**
    - Support `missing_value_encodings` as a new field of `model_info` object.
### 1.4.1
  - #### **Modifications**
    - Minor bug fix to handle string nan

### 1.4.0
  - #### **Modifications**
    - Default client initiation is now the v2 client
    - `publish_events_batch` is now async, returns status id and doesn't wait for the upload to complete.
    - Default behavior of all publish data in v2 client is async (`is_sync = False`)

### 1.3.0
  - #### **New Features**
    - New capabilities for Artifact-less Monitoring

### 1.2.8
  - ### **Modifications**
    - Change the `batch_size` argument default to 1000 for `trigger_pre_computation`
    - Updated the `delete_model` API default value for the `delete_prod` parameter from False to True.
      - We will by default delete all the events associated with the model.


### 1.2.7
  - ### **Modifications**
    - Added check for "model" key before access in from_dict
    - Allow changing artifact_status when updating the model
    - Adds docstrings for add_model, add_model_surrogate and add_model_artifact

### 1.2.6
  - ### **Modifications**
    - Fixed publish_events_batch_schema backward compatible.

### 1.2.5
  - ### **Modifications**
    - Added add_model_surrogate and add_model_artifact APIs for artifactless monitoring
    - Simplifies the add_model API by removing unnecessary parameters
    - Fixed publish_events_batch_schema parameter names.


### 1.2.4
  - ### **Modifications**
    - Fixed a type coercion bug that caused some get_slice calls to fail cryptically

### 1.2.3
  - ### **Modifications**
    - Map Tree shap values from log odds space to probability space
    - Added add_model API for artifactless monitoring
    - Fixed bug in request when creating a model using add_model

### 1.2.2
  - ### **Modifications**
    - Fixed a bug that prevented importing the client in some environments.

### 1.2.1
  - ### **Modifications**
    - Removed unnecessary server-client version check that produced an uninformative warning.

### 1.2.0
  - #### **New Features**
    - New `WeightingParams` object. This enables weighted histograms for class-imbalanced models.
  - #### **Modifications**
    - `update_model` allows some small modifications in model info for the following fields: custom_explanation_names, preferred_explanation_method, display_name, description, framework, algorithm and model_deployment_params


### 1.1.0
  - #### **New Features**
    - Add v2 client. v2 methods can be accessed either via sub-module (`client.v2.`) or by instantiating the `FiddlerApi` and passing `version=2`.
  - #### **Modifications**
    - Remove handlers from root logger
    - Add url, org_id, auth_token and version validation while instantiating client
    - Fix dataset ingestion file extension issue
    - init monitoring issue
    - Fix publish_event request header bug
    - Add `publish_events_batch_dataframe` and `upload_dataset_dataframe` methods
    - Support for DatasetInfo class
    - Using `http_client` package. A wrapper over `requetsts`.

### 1.0.6
   - #### **Modifications**
       - Add client v2 sub-package.
### 1.0.5
   - ##### **Modifications**
      - relax the version requirements for `requests`.
      - adds flag to init_monitoring to enable synchronous initialization
### 1.0.4
   - ##### **Modifications**
      - Fixed the JSON transformation issue which was forcing `requests` package upgrade issue
### 1.0.3
   - ##### **New Features**
      - Tree SHAP Helper.
  - ##### **Modifications**
      - `fdl.ModelInfo` has an additional optional parameter to enabled Tree Shap

### 1.0.2
   - ##### **New Features**
      - Integrated Gradients Keras TF2 Helpers.
   - ##### **Modifications**
      - Relax `botocore` version requirements.

### 1.0.1
   - ##### **Modifications**
      - Minor bug fixes and improvements.
      - `run_explanation`  has two additional optional arguments (`n_permutation` and `n_background`) allowing users to change the default parameters for Fiddler SHAP explanations.

### 1.0.0

Inaugural client for Fiddler 22.0! This version includes numerous improvements for stability, performance, and usability.

Compatible with server versions >=22.0.0.

### 0.8.1.8
   - ##### **Modifications**
      - Minor bug fixes and improvements.

### 0.8.1.7
   - ##### **Modifications**
      - Minor bug fixes and improvements.

### 0.8.1.6
   - ##### **Modifications**
      -  Add a parameter in list_projects API to get detailed project information
      - Minor bug fix for the datetime format.

### 0.8.1.5
   - ##### **Modifications**
      - Add a parameter in list_projects API to get detailed project information
      - Allow `run_explanation` api call to pass a list of explanation with `ig_flex` and one of the shap algorithm

### 0.8.1.4
   - ##### **Modifications**
      - Minor bugfix for categorical feature drift

### 0.8.1.3
   - ##### **Modifications**
      - Addressed an issue with categorical features with string literals containing numeric content

### 0.8.1.2
   - ##### **Modifications**
      - Implement a ranking surrogate model for ranking task models

### 0.8.1.1
   - ##### **Modifications**
      - change the dependecy of requests package to 0.25.1

### 0.8.1
   - ##### **Modifications**
      - Improved `SegmentInfo` validation.
      - make the dependency versions less strict.

### 0.8.0
   - ##### **New Features**
       - New `publish_events_batch_schema` API call, Publishes a batch events object to Fiddler Service using the passed `publish_schema` as a template.
       - New Ranking Monitoring capability available with publish_events_batch API
   - ##### **Modifications**
      - Enforced package versions in setup.py
      - `trigger_pre_computation` has an additional optional argument (`cache_dataset`) to enable/disable dataset histograms caching.
      - `register_model` has 3 additional optional arguments to enable/disable pdp caching (set to False by default), feature importance caching (set to True by default) and dataset histograms caching (set to True by default).

### 0.7.6
   - ##### **New Features**
       - New segment monitoring related functionality (currently in preview):
          - Ability to create and validate `SegmentInfo` objects,
          - `upload_segment` BE call,
          - `activate_segment` BE call,
          - `deactivate_segment` BE call, and
          - `list_segments` BE call,
   - ##### **Modifications**
       - Upon connecting to the server, the client now performs a version check for the *server* by default. Earlier the default was to only do a version check for the client.

### 0.7.5
   - ##### **New Features**
       - New `update_event` parameter for `publish_events_batch` API.
       - Changes to `fdl.publish_event()`:
           - Renamed parameter `event_time_stamp` to `event_timestamp`
           - Added new parameter: `timestamp_format`
               - Allows specification of timestamp format using the `FiddlerTimestamp` class

### 0.7.4
   - ##### **New Features**
       - New `initialize_monitoring` API call, sets up monitoring for a model. Intended to also work retroactively for legacy schema.
   - ##### **Modifications**
       - Modified `DatasetInfo.from_dataframe` and `ModelInfo.from_dataset_info` to take additional `dataset_id` as parameter.
       - Modified the `outputs` parameter of `ModelInfo.from_dataset_info` to now expect a dictionary in case of regression tasks, specifying output range.
       - Modified the `preferred_explanation_method` parameter of `ModelInfo.from_dataset_info` to accept string names from `custom_explanation_names`. Details in docstring.
       - Misc bug fixes and documentation enhancements.

### 0.7.3
   - ##### **New Features**
       - Changed the default display for `ModelInfo` and `DatasetInfo` to render HTML instead of plaintext, when accessed via jupyter notebooks
       - Added support for GCP Storage ingestion of log events using `fdl.BatchPublishType.GCP_STORAGE`

### 0.7.2
   - ##### **New Features**
       - Restructured the following arguments for `fdl.ModelInfo.from_dataset_info()`
           - Added: `categorical_target_class_details`:
               - Mandatory for Multiclass classification tasks, optional for Binary (unused for Regression)
               - Used to specify the positive class for Binary classification, and the class order for Multiclass classification
           - Modified: `target`:
               - No longer optional, models must specify target columns

### 0.7.1
   - ##### **New Features**
       - Restructured the following arguments for `fdl.publish_events_batch()`
           - Added: `id_field`:
               - Column to extract `id` value from
           - Added: `timestamp_format`:
               - Format of timestamp within batch object. Can be one of:
                    - `fdl.FiddlerTimestamp.INFER`
                    - `fdl.FiddlerTimestamp.EPOCH_MILLISECONDS`
                    - `fdl.FiddlerTimestamp.EPOCH_SECONDS`
                    - `fdl.FiddlerTimestamp.ISO_8601`
           Removed: `default_timestamp`
       - Minor bug fixes
   - ##### **Deprecation Warning**
       - Support `fdl.publish_events_log` and `fdl.publish_parquet_s3` will soon be
         deprecated in favor of `fdl.publish_events_batch()`


### 0.7.0
   - ##### **Dataset Refactor**
       -  Datasets refactored to be members of a Project
           - *This is a change promoting Datasets to be first class within Fiddler. It will affects both the UI and several API in Fiddler*
       - Many API utilizing Projects will now require `project_id` passed as a parameter
   - ##### **New Features**
       - Added `fdl.update_model()` to client
           - *update the specified model, with model binary and package.py from
              the specified model_dir*
       - Added `fdl.get_model()` to client
           - *download the model binary, package.py and model.yaml to the given
              output dir.*
       - Added `fdl.publish_events_batch()` to client
           - *Publishes a batch events object to Fiddler Service.*
           - *Note: Support for other batch methods including `fdl.publish_events_log()`
              and `fdl.publish_parquet_s3()` will be deprecated in the near future
              in favor of `fdl.publish_events_batch()`*
   - ##### **Changes**
       - Simplified logic within `fld.upload-dataset()`
       - Added client/server handshake for checking version compatibilities
           - *Warning issued in case of mismatch*
       - Deleted redundant APIs
           - `fdl.create_surrogate_model()`
           - `fdl.upload_model_sklearn()`
       - Restructured APIs to be more duck typing-friendly (relaxing data type restrictions)
       - Patches for minor bug-fixes


### 0.6.18
   - ##### **Features**
       - Minor updates to ease use of binary classification labels

### 0.6.17
   - ##### **Features**
       - Added new arguments to `ModelInfo.from_dataset_info()`
           - `preferred_explanation_method` to express a preferred default explanation algorithm for a model
           - `custom_explanation_names` to support user-provided explanation algorithms which the user will implement on their model object via package.py.

### 0.6.16
   - ##### **Features**
       - Minor improvements to `publish_events_log()` to circumvent datatype conversion issues

### 0.6.15
   - ##### **Features**
       - Added strict name checks

### 0.6.14
   - ##### **Features**
       - Added client-native multithreading support for `publish_events_log()`
       using new parameters `num_threads` and `batch_size`

### 0.6.13
   - ##### **Features**
       - Added `fdl.generate_sample_events()` to client
         -  *API for generating monitoring traffic to test out Fiddler*
       - Added `fdl.trigger_pre_computation()` to client
         -  *Triggers various precomputation steps within the Fiddler service based on input parameters.*
       -  Optionally add proxies to FiddlerApi() init

### 0.6.12
   - ##### **Features**
       - Added `fdl.publish_parquet_s3()` to client
         -  *Publishes parquet events file from S3 to Fiddler instance.
            Experimental and may be expanded in the future.*

### 0.6.10
   - ##### **Features**
       - Added `fdl.register_model()` to client
           -  *Register a model in fiddler. This will generate a surrogate model,
               which can be replaced later with original model.*
