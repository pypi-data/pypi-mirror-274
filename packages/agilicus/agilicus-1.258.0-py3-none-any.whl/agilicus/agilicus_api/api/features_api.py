"""
    Agilicus API

    Agilicus is API-first. Modern software is controlled by other software, is open, is available for you to use the way you want, securely, simply.  The OpenAPI Specification in YAML format is available on [www](https://www.agilicus.com/www/api/agilicus-openapi.yaml) for importing to other tools.  A rendered, online viewable and usable version of this specification is available at [api](https://www.agilicus.com/api). You may try the API inline directly in the web page. To do so, first obtain an Authentication Token (the simplest way is to install the Python SDK, and then run `agilicus-cli --issuer https://MYISSUER get-token`). You will need an org-id for most calls (and can obtain from `agilicus-cli --issuer https://MYISSUER list-orgs`). The `MYISSUER` will typically be `auth.MYDOMAIN`, and you will see it as you sign-in to the administrative UI.  This API releases on Bearer-Token authentication. To obtain a valid bearer token you will need to Authenticate to an Issuer with OpenID Connect (a superset of OAUTH2).  Your \"issuer\" will look like https://auth.MYDOMAIN. For example, when you signed-up, if you said \"use my own domain name\" and assigned a CNAME of cloud.example.com, then your issuer would be https://auth.cloud.example.com.  If you selected \"use an Agilicus supplied domain name\", your issuer would look like https://auth.myorg.agilicus.cloud.  For test purposes you can use our [Python SDK](https://pypi.org/project/agilicus/) and run `agilicus-cli --issuer https://auth.MYDOMAIN get-token`.  This API may be used in any language runtime that supports OpenAPI 3.0, or, you may use our [Python SDK](https://pypi.org/project/agilicus/), our [Typescript SDK](https://www.npmjs.com/package/@agilicus/angular), or our [Golang SDK](https://git.agilicus.com/pub/sdk-go).  100% of the activities in our system our API-driven, from our web-admin, through our progressive web applications, to all internals: there is nothing that is not accessible.  For more information, see [developer resources](https://www.agilicus.com/developer).   # noqa: E501

    The version of the OpenAPI document: 2024.05.17
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from agilicus_api.api_client import ApiClient, Endpoint as _Endpoint
from agilicus_api.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from agilicus_api.model.error_message import ErrorMessage
from agilicus_api.model.feature_tag import FeatureTag
from agilicus_api.model.list_feature_tags_response import ListFeatureTagsResponse


class FeaturesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __add_feature_tag(
            self,
            feature_tag,
            **kwargs
        ):
            """Add a feature tag  # noqa: E501

            Adds a new feature tag.   # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.add_feature_tag(feature_tag, async_req=True)
            >>> result = thread.get()

            Args:
                feature_tag (FeatureTag):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                FeatureTag
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['feature_tag'] = \
                feature_tag
            return self.call_with_http_info(**kwargs)

        if self.add_feature_tag is None:
            self.add_feature_tag = _Endpoint(
                settings={
                    'response_type': (FeatureTag,),
                    'auth': [
                        'token-valid'
                    ],
                    'endpoint_path': '/v1/feature_tags',
                    'operation_id': 'add_feature_tag',
                    'http_method': 'POST',
                    'servers': None,
                },
                params_map={
                    'all': [
                        'feature_tag',
                    ],
                    'required': [
                        'feature_tag',
                    ],
                    'nullable': [
                    ],
                    'enum': [
                    ],
                    'validation': [
                    ]
                },
                root_map={
                    'validations': {
                    },
                    'allowed_values': {
                    },
                    'openapi_types': {
                        'feature_tag':
                            (FeatureTag,),
                    },
                    'attribute_map': {
                    },
                    'location_map': {
                        'feature_tag': 'body',
                    },
                    'collection_format_map': {
                    }
                },
                headers_map={
                    'accept': [
                        'application/json'
                    ],
                    'content_type': [
                        'application/json'
                    ]
                },
                api_client=api_client,
                callable=__add_feature_tag
            )

        def __delete_feature_tag(
            self,
            feature_tag_name,
            **kwargs
        ):
            """Delete a feature tag  # noqa: E501

            Delete a feature tag  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_feature_tag(feature_tag_name, async_req=True)
            >>> result = thread.get()

            Args:
                feature_tag_name (str): A feature tag name found in the path

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                None
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['feature_tag_name'] = \
                feature_tag_name
            return self.call_with_http_info(**kwargs)

        if self.delete_feature_tag is None:
            self.delete_feature_tag = _Endpoint(
                settings={
                    'response_type': None,
                    'auth': [
                        'token-valid'
                    ],
                    'endpoint_path': '/v1/feature_tags/{feature_tag_name}',
                    'operation_id': 'delete_feature_tag',
                    'http_method': 'DELETE',
                    'servers': None,
                },
                params_map={
                    'all': [
                        'feature_tag_name',
                    ],
                    'required': [
                        'feature_tag_name',
                    ],
                    'nullable': [
                    ],
                    'enum': [
                    ],
                    'validation': [
                        'feature_tag_name',
                    ]
                },
                root_map={
                    'validations': {
                        ('feature_tag_name',): {
                            'max_length': 32,
                            'min_length': 1,
                        },
                    },
                    'allowed_values': {
                    },
                    'openapi_types': {
                        'feature_tag_name':
                            (str,),
                    },
                    'attribute_map': {
                        'feature_tag_name': 'feature_tag_name',
                    },
                    'location_map': {
                        'feature_tag_name': 'path',
                    },
                    'collection_format_map': {
                    }
                },
                headers_map={
                    'accept': [
                        'application/json'
                    ],
                    'content_type': [],
                },
                api_client=api_client,
                callable=__delete_feature_tag
            )

        def __get_feature_tag(
            self,
            feature_tag_name,
            **kwargs
        ):
            """Get a feature tag  # noqa: E501

            Get a feature tag  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_feature_tag(feature_tag_name, async_req=True)
            >>> result = thread.get()

            Args:
                feature_tag_name (str): A feature tag name found in the path

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                FeatureTag
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['feature_tag_name'] = \
                feature_tag_name
            return self.call_with_http_info(**kwargs)

        if self.get_feature_tag is None:
            self.get_feature_tag = _Endpoint(
                settings={
                    'response_type': (FeatureTag,),
                    'auth': [
                        'token-valid'
                    ],
                    'endpoint_path': '/v1/feature_tags/{feature_tag_name}',
                    'operation_id': 'get_feature_tag',
                    'http_method': 'GET',
                    'servers': None,
                },
                params_map={
                    'all': [
                        'feature_tag_name',
                    ],
                    'required': [
                        'feature_tag_name',
                    ],
                    'nullable': [
                    ],
                    'enum': [
                    ],
                    'validation': [
                        'feature_tag_name',
                    ]
                },
                root_map={
                    'validations': {
                        ('feature_tag_name',): {
                            'max_length': 32,
                            'min_length': 1,
                        },
                    },
                    'allowed_values': {
                    },
                    'openapi_types': {
                        'feature_tag_name':
                            (str,),
                    },
                    'attribute_map': {
                        'feature_tag_name': 'feature_tag_name',
                    },
                    'location_map': {
                        'feature_tag_name': 'path',
                    },
                    'collection_format_map': {
                    }
                },
                headers_map={
                    'accept': [
                        'application/json'
                    ],
                    'content_type': [],
                },
                api_client=api_client,
                callable=__get_feature_tag
            )

        def __list_feature_tags(
            self,
            **kwargs
        ):
            """List all feature_tags  # noqa: E501

            List all feature_tags matching the provided query parameters. Perform keyset pagination by setting the page_at_name parameter to the name for the next page to fetch. Set it to `\"\"` to start from the beginning.   # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.list_feature_tags(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                limit (int): limit the number of rows in the response. [optional] if omitted the server will use the default value of 500
                name (str): Filters based on whether or not the items in the collection have the given name. . [optional]
                page_at_name (str): Pagination based query with the name as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_name` field from the list response. . [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ListFeatureTagsResponse
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            return self.call_with_http_info(**kwargs)

        if self.list_feature_tags is None:
            self.list_feature_tags = _Endpoint(
                settings={
                    'response_type': (ListFeatureTagsResponse,),
                    'auth': [
                        'token-valid'
                    ],
                    'endpoint_path': '/v1/feature_tags',
                    'operation_id': 'list_feature_tags',
                    'http_method': 'GET',
                    'servers': None,
                },
                params_map={
                    'all': [
                        'limit',
                        'name',
                        'page_at_name',
                    ],
                    'required': [],
                    'nullable': [
                    ],
                    'enum': [
                    ],
                    'validation': [
                        'limit',
                    ]
                },
                root_map={
                    'validations': {
                        ('limit',): {

                            'inclusive_maximum': 500,
                            'inclusive_minimum': 1,
                        },
                    },
                    'allowed_values': {
                    },
                    'openapi_types': {
                        'limit':
                            (int,),
                        'name':
                            (str,),
                        'page_at_name':
                            (str,),
                    },
                    'attribute_map': {
                        'limit': 'limit',
                        'name': 'name',
                        'page_at_name': 'page_at_name',
                    },
                    'location_map': {
                        'limit': 'query',
                        'name': 'query',
                        'page_at_name': 'query',
                    },
                    'collection_format_map': {
                    }
                },
                headers_map={
                    'accept': [
                        'application/json'
                    ],
                    'content_type': [],
                },
                api_client=api_client,
                callable=__list_feature_tags
            )

        def __replace_feature_tag(
            self,
            feature_tag_name,
            **kwargs
        ):
            """update a feature tag  # noqa: E501

            update a feature tag  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.replace_feature_tag(feature_tag_name, async_req=True)
            >>> result = thread.get()

            Args:
                feature_tag_name (str): A feature tag name found in the path

            Keyword Args:
                feature_tag (FeatureTag): [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                FeatureTag
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['feature_tag_name'] = \
                feature_tag_name
            return self.call_with_http_info(**kwargs)

        if self.replace_feature_tag is None:
            self.replace_feature_tag = _Endpoint(
                settings={
                    'response_type': (FeatureTag,),
                    'auth': [
                        'token-valid'
                    ],
                    'endpoint_path': '/v1/feature_tags/{feature_tag_name}',
                    'operation_id': 'replace_feature_tag',
                    'http_method': 'PUT',
                    'servers': None,
                },
                params_map={
                    'all': [
                        'feature_tag_name',
                        'feature_tag',
                    ],
                    'required': [
                        'feature_tag_name',
                    ],
                    'nullable': [
                    ],
                    'enum': [
                    ],
                    'validation': [
                        'feature_tag_name',
                    ]
                },
                root_map={
                    'validations': {
                        ('feature_tag_name',): {
                            'max_length': 32,
                            'min_length': 1,
                        },
                    },
                    'allowed_values': {
                    },
                    'openapi_types': {
                        'feature_tag_name':
                            (str,),
                        'feature_tag':
                            (FeatureTag,),
                    },
                    'attribute_map': {
                        'feature_tag_name': 'feature_tag_name',
                    },
                    'location_map': {
                        'feature_tag_name': 'path',
                        'feature_tag': 'body',
                    },
                    'collection_format_map': {
                    }
                },
                headers_map={
                    'accept': [
                        'application/json'
                    ],
                    'content_type': [
                        'application/json'
                    ]
                },
                api_client=api_client,
                callable=__replace_feature_tag
            )

    add_feature_tag = None 
    delete_feature_tag = None 
    get_feature_tag = None 
    list_feature_tags = None 
    replace_feature_tag = None 
