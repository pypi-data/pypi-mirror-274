"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from ultracart.model_utils import (  # noqa: F401
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
    OpenApiModel
)
from ultracart.exceptions import ApiAttributeError


def lazy_import():
    from ultracart.model.order import Order
    globals()['Order'] = Order


class ChargebackDispute(ModelNormal):
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
        ('account_number',): {
            'max_length': 50,
        },
        ('auth_code',): {
            'max_length': 20,
        },
        ('case_number',): {
            'max_length': 50,
        },
        ('currency',): {
            'max_length': 10,
        },
        ('encryption_key',): {
            'max_length': 100,
        },
        ('fax_failure_reason',): {
            'max_length': 250,
        },
        ('fax_number',): {
            'max_length': 20,
        },
        ('icsid',): {
            'max_length': 50,
        },
        ('order_id',): {
            'max_length': 30,
        },
        ('partial_card_number',): {
            'max_length': 20,
        },
        ('pdf_file_oid',): {
            'max_length': 32,
        },
        ('reason_code',): {
            'max_length': 70,
        },
        ('status',): {
            'max_length': 20,
        },
        ('website_url',): {
            'max_length': 250,
        },
    }

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
            'account_number': (str,),  # noqa: E501
            'adjustment_request_text': (str,),  # noqa: E501
            'amount': (float,),  # noqa: E501
            'auth_code': (str,),  # noqa: E501
            'case_number': (str,),  # noqa: E501
            'chargeback_dispute_oid': (int,),  # noqa: E501
            'chargeback_dts': (str,),  # noqa: E501
            'currency': (str,),  # noqa: E501
            'customer_care_notes': (str,),  # noqa: E501
            'encryption_key': (str,),  # noqa: E501
            'expiration_dts': (str,),  # noqa: E501
            'fax_failure_reason': (str,),  # noqa: E501
            'fax_number': (str,),  # noqa: E501
            'fax_transaction_id': (int,),  # noqa: E501
            'icsid': (str,),  # noqa: E501
            'merchant_account_profile_oid': (int,),  # noqa: E501
            'order': (Order,),  # noqa: E501
            'order_id': (str,),  # noqa: E501
            'partial_card_number': (str,),  # noqa: E501
            'pdf_file_oid': (str,),  # noqa: E501
            'reason_code': (str,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'website_url': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'account_number': 'account_number',  # noqa: E501
        'adjustment_request_text': 'adjustment_request_text',  # noqa: E501
        'amount': 'amount',  # noqa: E501
        'auth_code': 'auth_code',  # noqa: E501
        'case_number': 'case_number',  # noqa: E501
        'chargeback_dispute_oid': 'chargeback_dispute_oid',  # noqa: E501
        'chargeback_dts': 'chargeback_dts',  # noqa: E501
        'currency': 'currency',  # noqa: E501
        'customer_care_notes': 'customer_care_notes',  # noqa: E501
        'encryption_key': 'encryption_key',  # noqa: E501
        'expiration_dts': 'expiration_dts',  # noqa: E501
        'fax_failure_reason': 'fax_failure_reason',  # noqa: E501
        'fax_number': 'fax_number',  # noqa: E501
        'fax_transaction_id': 'fax_transaction_id',  # noqa: E501
        'icsid': 'icsid',  # noqa: E501
        'merchant_account_profile_oid': 'merchant_account_profile_oid',  # noqa: E501
        'order': 'order',  # noqa: E501
        'order_id': 'order_id',  # noqa: E501
        'partial_card_number': 'partial_card_number',  # noqa: E501
        'pdf_file_oid': 'pdf_file_oid',  # noqa: E501
        'reason_code': 'reason_code',  # noqa: E501
        'status': 'status',  # noqa: E501
        'website_url': 'website_url',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """ChargebackDispute - a model defined in OpenAPI

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
            account_number (str): Account number. [optional]  # noqa: E501
            adjustment_request_text (str): Adjustment request text. [optional]  # noqa: E501
            amount (float): Amount. [optional]  # noqa: E501
            auth_code (str): Auth code. [optional]  # noqa: E501
            case_number (str): Case number. [optional]  # noqa: E501
            chargeback_dispute_oid (int): Chargeback Dispute Oid. [optional]  # noqa: E501
            chargeback_dts (str): Chargeback dts. [optional]  # noqa: E501
            currency (str): Currency. [optional]  # noqa: E501
            customer_care_notes (str): Customer care notes. [optional]  # noqa: E501
            encryption_key (str): Encryption key. [optional]  # noqa: E501
            expiration_dts (str): Expiration Dts. [optional]  # noqa: E501
            fax_failure_reason (str): Fax failure reason. [optional]  # noqa: E501
            fax_number (str): Fax number. [optional]  # noqa: E501
            fax_transaction_id (int): Fax transaction id. [optional]  # noqa: E501
            icsid (str): icsid. [optional]  # noqa: E501
            merchant_account_profile_oid (int): Merchant account profile oid. [optional]  # noqa: E501
            order (Order): [optional]  # noqa: E501
            order_id (str): Order Id. [optional]  # noqa: E501
            partial_card_number (str): Partial card number. [optional]  # noqa: E501
            pdf_file_oid (str): PDF file oid. [optional]  # noqa: E501
            reason_code (str): Reason code. [optional]  # noqa: E501
            status (str): Status. [optional]  # noqa: E501
            website_url (str): Website URL. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
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

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """ChargebackDispute - a model defined in OpenAPI

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
            account_number (str): Account number. [optional]  # noqa: E501
            adjustment_request_text (str): Adjustment request text. [optional]  # noqa: E501
            amount (float): Amount. [optional]  # noqa: E501
            auth_code (str): Auth code. [optional]  # noqa: E501
            case_number (str): Case number. [optional]  # noqa: E501
            chargeback_dispute_oid (int): Chargeback Dispute Oid. [optional]  # noqa: E501
            chargeback_dts (str): Chargeback dts. [optional]  # noqa: E501
            currency (str): Currency. [optional]  # noqa: E501
            customer_care_notes (str): Customer care notes. [optional]  # noqa: E501
            encryption_key (str): Encryption key. [optional]  # noqa: E501
            expiration_dts (str): Expiration Dts. [optional]  # noqa: E501
            fax_failure_reason (str): Fax failure reason. [optional]  # noqa: E501
            fax_number (str): Fax number. [optional]  # noqa: E501
            fax_transaction_id (int): Fax transaction id. [optional]  # noqa: E501
            icsid (str): icsid. [optional]  # noqa: E501
            merchant_account_profile_oid (int): Merchant account profile oid. [optional]  # noqa: E501
            order (Order): [optional]  # noqa: E501
            order_id (str): Order Id. [optional]  # noqa: E501
            partial_card_number (str): Partial card number. [optional]  # noqa: E501
            pdf_file_oid (str): PDF file oid. [optional]  # noqa: E501
            reason_code (str): Reason code. [optional]  # noqa: E501
            status (str): Status. [optional]  # noqa: E501
            website_url (str): Website URL. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
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
