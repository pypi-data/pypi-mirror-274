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
    from agilicus_api.model.admin_status import AdminStatus
    from agilicus_api.model.application_upstream_form_info import ApplicationUpstreamFormInfo
    from agilicus_api.model.application_upstream_validation import ApplicationUpstreamValidation
    from agilicus_api.model.auto_create_status import AutoCreateStatus
    from agilicus_api.model.operational_status import OperationalStatus
    globals()['AdminStatus'] = AdminStatus
    globals()['ApplicationUpstreamFormInfo'] = ApplicationUpstreamFormInfo
    globals()['ApplicationUpstreamValidation'] = ApplicationUpstreamValidation
    globals()['AutoCreateStatus'] = AutoCreateStatus
    globals()['OperationalStatus'] = OperationalStatus


class ApplicationUpstreamIdentityProvider(ModelNormal):
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
        ('upstream_type',): {
            'OIDC': "oidc",
            'LOCAL_AUTH': "local_auth",
            'APPLICATION': "application",
            'KERBEROS': "kerberos",
        },
    }

    validations = {
        ('name',): {
            'max_length': 100,
            'min_length': 1,
        },
        ('issuer',): {
            'max_length': 511,
            'min_length': 1,
        },
        ('icon',): {
            'max_length': 50,
            'regex': {
                'pattern': r'^$|^[0-9a-zA-Z-_.]+$',  # noqa: E501
            },
        },
    }

    @property
    def name(self):
       return self.get("name")

    @name.setter
    def name(self, new_value):
       self.name = new_value

    @property
    def issuer(self):
       return self.get("issuer")

    @issuer.setter
    def issuer(self, new_value):
       self.issuer = new_value

    @property
    def upstream_type(self):
       return self.get("upstream_type")

    @upstream_type.setter
    def upstream_type(self, new_value):
       self.upstream_type = new_value

    @property
    def icon(self):
       return self.get("icon")

    @icon.setter
    def icon(self, new_value):
       self.icon = new_value

    @property
    def auto_create_status(self):
       return self.get("auto_create_status")

    @auto_create_status.setter
    def auto_create_status(self, new_value):
       self.auto_create_status = new_value

    @property
    def admin_status(self):
       return self.get("admin_status")

    @admin_status.setter
    def admin_status(self, new_value):
       self.admin_status = new_value

    @property
    def trap_disabled(self):
       return self.get("trap_disabled")

    @trap_disabled.setter
    def trap_disabled(self, new_value):
       self.trap_disabled = new_value

    @property
    def operational_status(self):
       return self.get("operational_status")

    @operational_status.setter
    def operational_status(self, new_value):
       self.operational_status = new_value

    @property
    def validation(self):
       return self.get("validation")

    @validation.setter
    def validation(self, new_value):
       self.validation = new_value

    @property
    def form_info(self):
       return self.get("form_info")

    @form_info.setter
    def form_info(self, new_value):
       self.form_info = new_value

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
            'validation': (ApplicationUpstreamValidation,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'issuer': (str,),  # noqa: E501
            'upstream_type': (str,),  # noqa: E501
            'icon': (str,),  # noqa: E501
            'auto_create_status': (AutoCreateStatus,),  # noqa: E501
            'admin_status': (AdminStatus,),  # noqa: E501
            'trap_disabled': (bool,),  # noqa: E501
            'operational_status': (OperationalStatus,),  # noqa: E501
            'form_info': (ApplicationUpstreamFormInfo,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None



    attribute_map = {
        'validation': 'validation',  # noqa: E501
        'name': 'name',  # noqa: E501
        'issuer': 'issuer',  # noqa: E501
        'upstream_type': 'upstream_type',  # noqa: E501
        'icon': 'icon',  # noqa: E501
        'auto_create_status': 'auto_create_status',  # noqa: E501
        'admin_status': 'admin_status',  # noqa: E501
        'trap_disabled': 'trap_disabled',  # noqa: E501
        'operational_status': 'operational_status',  # noqa: E501
        'form_info': 'form_info',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, validation, *args, **kwargs):  # noqa: E501
        """ApplicationUpstreamIdentityProvider - a model defined in OpenAPI

        Args:
            validation (ApplicationUpstreamValidation):

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
            name (str): A name used to uniquely refer to the upstream identity provider configuration. This is the text that will be displayed when presenting the upstream identity for login.. [optional]  # noqa: E501
            issuer (str): The upstream issuer uri. This is the URI which identifies the issuer against which users selecting this upstream will authenticate.. [optional]  # noqa: E501
            upstream_type (str): The type of upstream. For instance an OpenID Connector Upstream.. [optional]  # noqa: E501
            icon (str): The icon file to be used, limited to: numbers, letters, underscores, hyphens and periods. It is part of a css class (with the periods replaced by underscores).  To use a custom icon than the provided default you will need to add the icon the static/img folder and update the static css file to add a new css button like below ```json .dex-btn-icon--<your-logo_svg> {   background-image: url(../static/img/<your-logo.svg>); } ```  To use a default icon simply enter an icon name from the pre-provided defaults found in the static/img folder The default icons are   - bitbucket   - coreos   - email   - github   - gitlab   - google   - ldap   - linkedin   - microsoft   - oidc   - saml . [optional]  # noqa: E501
            auto_create_status (AutoCreateStatus): [optional]  # noqa: E501
            admin_status (AdminStatus): [optional]  # noqa: E501
            trap_disabled (bool): Inidicates whether traps (notifications) should be disabled for this entity. A true state indicates notifications will not be sent on transition. . [optional]  # noqa: E501
            operational_status (OperationalStatus): [optional]  # noqa: E501
            form_info (ApplicationUpstreamFormInfo): [optional]  # noqa: E501
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

        self.validation = validation
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
    def __init__(self, validation, *args, **kwargs):  # noqa: E501
        """ApplicationUpstreamIdentityProvider - a model defined in OpenAPI

        Args:
            validation (ApplicationUpstreamValidation):

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
            name (str): A name used to uniquely refer to the upstream identity provider configuration. This is the text that will be displayed when presenting the upstream identity for login.. [optional]  # noqa: E501
            issuer (str): The upstream issuer uri. This is the URI which identifies the issuer against which users selecting this upstream will authenticate.. [optional]  # noqa: E501
            upstream_type (str): The type of upstream. For instance an OpenID Connector Upstream.. [optional]  # noqa: E501
            icon (str): The icon file to be used, limited to: numbers, letters, underscores, hyphens and periods. It is part of a css class (with the periods replaced by underscores).  To use a custom icon than the provided default you will need to add the icon the static/img folder and update the static css file to add a new css button like below ```json .dex-btn-icon--<your-logo_svg> {   background-image: url(../static/img/<your-logo.svg>); } ```  To use a default icon simply enter an icon name from the pre-provided defaults found in the static/img folder The default icons are   - bitbucket   - coreos   - email   - github   - gitlab   - google   - ldap   - linkedin   - microsoft   - oidc   - saml . [optional]  # noqa: E501
            auto_create_status (AutoCreateStatus): [optional]  # noqa: E501
            admin_status (AdminStatus): [optional]  # noqa: E501
            trap_disabled (bool): Inidicates whether traps (notifications) should be disabled for this entity. A true state indicates notifications will not be sent on transition. . [optional]  # noqa: E501
            operational_status (OperationalStatus): [optional]  # noqa: E501
            form_info (ApplicationUpstreamFormInfo): [optional]  # noqa: E501
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

        self.validation = validation
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

