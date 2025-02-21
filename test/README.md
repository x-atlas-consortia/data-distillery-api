# Data Distillery API

## Test scripts

### Background

#### UBKG API deployment 
The data-distillery-api is a [child UBKG API](https://ubkg.docs.xconsortia.org/api/#child-ubkg-api-instances). 
The data-distillery-api contains code for endpoints that work with a UBKG instance in the Data Distillery [context](https://ubkg.docs.xconsortia.org/contexts/)--
i.e., with data specific to Data Distillery; however, it also accepts calls to endpoints of the
generic UBKG base context. The code for generic endpoints is stored in the ubkg-api; 
the data-distillery-api integrates with the ubkg-api that is compiled as a library 
(PyPi package).

A **UBKG API deployment** corresponds to the combination of the ubkg-api and one or more child APIs. 
The HuBMAP/SenNet UBKG API deployment combines ubkg-api and hs-ontology-api.

#### API Gateway
The endpoint URLs for the Data Distillery UBKG API deployment are managed by a AWS API Gateway.
The gateway manages the union of all endpoint URLs.

### Types of Testing

#### Endpoints: unit and regression testing
To unit test or regression test endpoints of a UBKG API deployment, the developer should
work within the API instance that houses the endpoint code. In other words,
test data-distillery-api endpoints by instantiating data-distillery-api; test ubkg-api
endpoints by instantiating ubkg-api. 

In particular, testing new functionality in ubkg-api by executing against an instance
of data-distillery-api is not a valid test methodology. Because the data-distillery-api
works with a compiled package version of ubkg-api, it is better to test ubkg-api
endpoints in a development ubkg-api instance; once the ubkg-api endpoint is validated, the 
ubkg-api package can be recompiled for use by the data-distillery-api.

To test data-distillery-api endpoints, use the **test_api.s**h script in this folder. 
The script writes output to the test.out file, which is ignored by git.

#### Gateway: integration testing
Because the API gateway manages the endpoint URLs of all components of a UBKG API instance, it
is often necessary to test the union of endpoint URLs. This is not a functional test of a particular endpoint; 
instead, it is an integration test of the gateway configuration.

To test the gateway for the Data Distillery UBKG API deployment, use the **test_gateway.sh** script in this folder.

# Optional Timeout Feature

When deployed behind a server gateway, such as AWS API Gateway, the gateway may impose constraints
on timeout. For example, AWS API Gateway has a timeout of 29 seconds.

The ubkg-api (loaded as a library by the data-distillery-api) can handle timeouts before they result in errors in a gateway. 
The ubkg-api can return detailed explanations for timeout issues, instead of relying on the 
sometimes ambiguous messages from the gateway (e.g., a HTTP 500).

To enable custom management of timeout, specify values in the **app.cfg** file, as shown below.

```commandline
# Maximum duration for the execution of timeboxed queries to prevent service timeout, in seconds
# The AWS API gateway timeout is 29 seconds.
TIMEOUT=28
```

# Managing large payloads
When deployed behind a server gateway, such as AWS API Gateway, the gateway may impose constraints
on the size of response payload. For example, AWS API Gateway has a response payload limit of 10 MB.

The ubkg-api (loaded as a library by the data-distillery-api) can return a custom
HTTP 413 error (Payload too Large) when the response exceeds a specified threshold.
The data-distillery-api can override the default threshold in its app.cfg file:
```commandline
LARGE_RESPONSE_THRESHOLD = 9*(2**20) + 900*(2**10) #9.9Mb
```

# Optional S3 redirection for large payloads
The ubkg-api can redirect large responses to a file 
in a AWS S3 bucket. Endpoints enabled for S3 redirection will return a 
URL that points to the file in the S3 bucket. The URL is "pre-signed": consumers can simply
"get" the URL to download the file locally.

By default, the ubkg-api does not redirect large responses. To enable S3 redirection, specify values in 
the **app.cfg** file of data-distillery-api.

```commandline
# Large response threshold, as determined by the length of the response (payload).
# Responses with payload sizes that exceed the threshold will be handled in one of the
# following ways:
# 1. If the threshold is 0, then the response will be passed without any additional processing.
# 2. If the threshold is nonzero and S3 redirection is not enabled, the API will return
#    a custom HTTP 413 response.
# 3. If the threshold is nonzero and S3 redirection is enabled, the API will stash the
#    response in a file in an S3 bucket and return a pre-signed URL pointing to the
#    stashed file.
# Setting the threshold to 9.9MB avoids triggering a HTTP 500 from an AWS API Gateway's hard
# 10 MB payload limit
LARGE_RESPONSE_THRESHOLD = 9*(2**20) + 900*(2**10) #9.9Mb

# OPTIONAL AWS credentials for S3 redirection. If there are no "AWS_*" keys, the
# API will return the default HTTP 413 exception.
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
# This is new IAM user hubmap-api-s3-prod created on 10/3/2024
AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_S3_BUCKET_NAME = 'AWS_S3_BUCKET_NAME'
AWS_S3_OBJECT_PREFIX = 'AWS_S3_OBJECT_PREFIX'
AWS_OBJECT_URL_EXPIRATION_IN_SECS = 60*60 # 1 hour
