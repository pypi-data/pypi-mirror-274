"""
    Agilicus API

    Agilicus is API-first. Modern software is controlled by other software, is open, is available for you to use the way you want, securely, simply.  The OpenAPI Specification in YAML format is available on [www](https://www.agilicus.com/www/api/agilicus-openapi.yaml) for importing to other tools.  A rendered, online viewable and usable version of this specification is available at [api](https://www.agilicus.com/api). You may try the API inline directly in the web page. To do so, first obtain an Authentication Token (the simplest way is to install the Python SDK, and then run `agilicus-cli --issuer https://MYISSUER get-token`). You will need an org-id for most calls (and can obtain from `agilicus-cli --issuer https://MYISSUER list-orgs`). The `MYISSUER` will typically be `auth.MYDOMAIN`, and you will see it as you sign-in to the administrative UI.  This API releases on Bearer-Token authentication. To obtain a valid bearer token you will need to Authenticate to an Issuer with OpenID Connect (a superset of OAUTH2).  Your \"issuer\" will look like https://auth.MYDOMAIN. For example, when you signed-up, if you said \"use my own domain name\" and assigned a CNAME of cloud.example.com, then your issuer would be https://auth.cloud.example.com.  If you selected \"use an Agilicus supplied domain name\", your issuer would look like https://auth.myorg.agilicus.cloud.  For test purposes you can use our [Python SDK](https://pypi.org/project/agilicus/) and run `agilicus-cli --issuer https://auth.MYDOMAIN get-token`.  This API may be used in any language runtime that supports OpenAPI 3.0, or, you may use our [Python SDK](https://pypi.org/project/agilicus/), our [Typescript SDK](https://www.npmjs.com/package/@agilicus/angular), or our [Golang SDK](https://git.agilicus.com/pub/sdk-go).  100% of the activities in our system our API-driven, from our web-admin, through our progressive web applications, to all internals: there is nothing that is not accessible.  For more information, see [developer resources](https://www.agilicus.com/developer).   # noqa: E501

    The version of the OpenAPI document: 2024.05.17
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from agilicus_api.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from agilicus_api.exceptions import ApiAttributeError


def lazy_import():
    from agilicus_api.model.audit_destination_authentication import AuditDestinationAuthentication
    from agilicus_api.model.audit_destination_filter import AuditDestinationFilter
    globals()['AuditDestinationAuthentication'] = AuditDestinationAuthentication
    globals()['AuditDestinationFilter'] = AuditDestinationFilter


class AuditDestinationSpec(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('name',): {
            'max_length': 128,
        },
        ('max_events_per_transaction',): {
            'inclusive_minimum': 1,
        },
    }

    @property
    def enabled(self):
       return self.get("enabled")

    @enabled.setter
    def enabled(self, new_value):
       self.enabled = new_value

    @property
    def name(self):
       return self.get("name")

    @name.setter
    def name(self, new_value):
       self.name = new_value

    @property
    def org_id(self):
       return self.get("org_id")

    @org_id.setter
    def org_id(self, new_value):
       self.org_id = new_value

    @property
    def destination_type(self):
       return self.get("destination_type")

    @destination_type.setter
    def destination_type(self, new_value):
       self.destination_type = new_value

    @property
    def location(self):
       return self.get("location")

    @location.setter
    def location(self, new_value):
       self.location = new_value

    @property
    def max_events_per_transaction(self):
       return self.get("max_events_per_transaction")

    @max_events_per_transaction.setter
    def max_events_per_transaction(self, new_value):
       self.max_events_per_transaction = new_value

    @property
    def comment(self):
       return self.get("comment")

    @comment.setter
    def comment(self, new_value):
       self.comment = new_value

    @property
    def filters(self):
       return self.get("filters")

    @filters.setter
    def filters(self, new_value):
       self.filters = new_value

    @property
    def authentication(self):
       return self.get("authentication")

    @authentication.setter
    def authentication(self, new_value):
       self.authentication = new_value

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'enabled': (bool,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'org_id': (str,),  # noqa: E501
            'destination_type': (str,),  # noqa: E501
            'location': (str,),  # noqa: E501
            'comment': (str,),  # noqa: E501
            'filters': ([AuditDestinationFilter],),  # noqa: E501
            'max_events_per_transaction': (int,),  # noqa: E501
            'authentication': (AuditDestinationAuthentication,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None



    attribute_map = {
        'enabled': 'enabled',  # noqa: E501
        'name': 'name',  # noqa: E501
        'org_id': 'org_id',  # noqa: E501
        'destination_type': 'destination_type',  # noqa: E501
        'location': 'location',  # noqa: E501
        'comment': 'comment',  # noqa: E501
        'filters': 'filters',  # noqa: E501
        'max_events_per_transaction': 'max_events_per_transaction',  # noqa: E501
        'authentication': 'authentication',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, enabled, name, org_id, destination_type, location, comment, filters, *args, **kwargs):  # noqa: E501
        """AuditDestinationSpec - a model defined in OpenAPI

        Args:
            enabled (bool): Whether to sent events to the AuditDestination at all. Setting `enabled` to `false` will direct all event sources to stop sending events to the AuditDestination. 
            name (str): A descriptive name for the destination. This will be used in reporting and diagnostics. 
            org_id (str): Unique identifier
            destination_type (str): The type of the destination. This controls how events are sent to the destination. This can be set to the following values:  - `file`: A file destination. The url is the path to a file on disk where events will be logged. The log format is JSONL. The log file is rotated. Old rotations are placed in the same directory as the log file. - `webhook`: A webhook destination. The url is points to an http server which will accept POSTs of an   AuditWebhookEvent object. The server should respond with an HTTP 2XX return code on success. The   event should be handled as a transaction: either all events are processed, or none. An HTTP 429   in conjunction with a Retry-After header may be used to tell the audit agent to back off. An HTTP   400 will instruct the audit agent to discard all of the events. 
            location (str): The location of the destination. The meaning of the location changes based on the destination type.  - `file`: A URL of the path to the file on the local system. The URL should be of the form `file:///path/to/file`.    On Windows this can be `/drive/path/to/file`.  If the path is relative (`file://./path/to/file`), the relative path is    rooted at the directory from which the evnet source is running. 
            comment (str): A short comment describing the purpose of the destination. This is only used for informational purposes. 
            filters ([AuditDestinationFilter]): The list of filters controlling which events are sent to this destination. All filters must pass in order to send an event to this destination. 

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            max_events_per_transaction (int): The maximum number of events to emit to destination in one transaction. If unspecified, the value is unlimited. This can be useful if the destination (e.g. a webhook) has a maximum request size. . [optional]  # noqa: E501
            authentication (AuditDestinationAuthentication): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.enabled = enabled
        self.name = name
        self.org_id = org_id
        self.destination_type = destination_type
        self.location = location
        self.comment = comment
        self.filters = filters
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    def __python_set(val):
        return set(val)
 
    required_properties = __python_set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, enabled, name, org_id, destination_type, location, comment, filters, *args, **kwargs):  # noqa: E501
        """AuditDestinationSpec - a model defined in OpenAPI

        Args:
            enabled (bool): Whether to sent events to the AuditDestination at all. Setting `enabled` to `false` will direct all event sources to stop sending events to the AuditDestination. 
            name (str): A descriptive name for the destination. This will be used in reporting and diagnostics. 
            org_id (str): Unique identifier
            destination_type (str): The type of the destination. This controls how events are sent to the destination. This can be set to the following values:  - `file`: A file destination. The url is the path to a file on disk where events will be logged. The log format is JSONL. The log file is rotated. Old rotations are placed in the same directory as the log file. - `webhook`: A webhook destination. The url is points to an http server which will accept POSTs of an   AuditWebhookEvent object. The server should respond with an HTTP 2XX return code on success. The   event should be handled as a transaction: either all events are processed, or none. An HTTP 429   in conjunction with a Retry-After header may be used to tell the audit agent to back off. An HTTP   400 will instruct the audit agent to discard all of the events. 
            location (str): The location of the destination. The meaning of the location changes based on the destination type.  - `file`: A URL of the path to the file on the local system. The URL should be of the form `file:///path/to/file`.    On Windows this can be `/drive/path/to/file`.  If the path is relative (`file://./path/to/file`), the relative path is    rooted at the directory from which the evnet source is running. 
            comment (str): A short comment describing the purpose of the destination. This is only used for informational purposes. 
            filters ([AuditDestinationFilter]): The list of filters controlling which events are sent to this destination. All filters must pass in order to send an event to this destination. 

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            max_events_per_transaction (int): The maximum number of events to emit to destination in one transaction. If unspecified, the value is unlimited. This can be useful if the destination (e.g. a webhook) has a maximum request size. . [optional]  # noqa: E501
            authentication (AuditDestinationAuthentication): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.enabled = enabled
        self.name = name
        self.org_id = org_id
        self.destination_type = destination_type
        self.location = location
        self.comment = comment
        self.filters = filters
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")

