import re
from typing import Optional, Union

from pyawsopstoolkit.exceptions import ValidationError


def _check_type(value, expected_type, raise_error, error_message):
    """
    Checks if the given value has the expected type.
    :param value: The value to be checked.
    :type value: Any
    :param expected_type: The expected type for the value.
    :type expected_type: type
    :param raise_error: Flag indicating whether to raise an error if the type check fails.
    :type raise_error: bool
    :param error_message: The error message to be raised if the type check fails and raise_error is True.
    :type error_message: str
    :return: True if the value has the expected type, False otherwise.
    :rtype: bool
    """
    if not isinstance(value, expected_type):
        if raise_error:
            raise TypeError(error_message)
        return False

    return True


class AccountValidator:
    """
    A class for validating AWS account information.
    This class provides methods to validate various aspects of account information, such as account numbers.
    """
    # Regular expression pattern for validating account numbers.
    # The pattern ensures that the account number consists of exactly 12 digits.
    NUMBER_PATTERN: str = r'^\d{12}$'

    @classmethod
    def _get_error_message(
            cls,
            variable_name: str,
            variable_type: str,
            custom_error_message: Optional[str] = None
    ) -> str:
        """
        Get the error message for the validation.
        :param variable_name: Name of the variable being validated.
        :type variable_name: str
        :param variable_type: Expected type of the variable.
        :type variable_type: str
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: Error message.
        :rtype: str
        """
        return custom_error_message or (
            f'{variable_name} should be of {variable_type}. Refer to '
            f'https://docs.aws.amazon.com/organizations/latest/APIReference/API_DescribeAccount.html '
            f'for more information.'
        )

    @classmethod
    def number(
            cls,
            value: str,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate the account number.
        :param value: Account number to validate.
        :type value: str
        :param raise_error: Flag indicating whether to raise an error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation succeeds, False otherwise.
        :rtype: bool
        """
        _check_type(value, str, True, 'value should be a string.')
        _check_type(raise_error, Union[bool, None], True, 'raise_error should be a boolean.')
        _check_type(custom_error_message, Union[str, None], True, 'custom_error_message should be a boolean.')

        error_message = cls._get_error_message(value, 'string', custom_error_message)

        if not _check_type(value, str, raise_error, error_message) or not re.match(cls.NUMBER_PATTERN, value):
            if raise_error:
                raise ValidationError(error_message)
            return False

        return True


class ArnValidator:
    """
    Validates AWS ARNs (Amazon Resource Names) according to the AWS ARN format.
    This class provides methods to validate various aspects of ARNs, such as partition, service, region, account ID,
    and resource ID.
    """
    # Regular expression pattern for AWS ARNs
    ARN_PATTERN: str = (
        r'arn:'  # arn
        r'(aws|aws-cn|aws-us-gov):'  # partition
        r'([a-z0-9-]+):'  # service
        r'([a-z0-9-]+)?:'  # region (optional for global services)
        r'([0-9]{12})?:'  # account id (option for s3)
        r'([a-zA-Z0-9-_:/\*]+)'  # resource id or type
        r'(:[a-zA-Z0-9-_:/\*]+)*'  # resource id
    )

    @classmethod
    def _get_error_message(
            cls,
            variable_name: str,
            variable_type: str,
            custom_error_message: Optional[str] = None
    ) -> str:
        """
        Get the error message for the validation.
        :param variable_name: Name of the variable being validated.
        :type variable_name: str
        :param variable_type: Expected type of the variable.
        :type variable_type: str
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: Error message.
        :rtype: str
        """
        return custom_error_message or (
            f'{variable_name} should be of {variable_type}. Refer to '
            f'https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html '
            f'for more information.'
        )

    @classmethod
    def _arn(
            cls,
            value: str,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate if the given string matches the ARN pattern.
        :param value: The string to be validated.
        :type value: str
        :param raise_error: Flag to raise an error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message to be used if raise_error is True and validation fails.
        :type custom_error_message: str
        :return: True if the string matches the ARN pattern, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('arn', 'string', custom_error_message)

        if not _check_type(value, str, raise_error, error_message) or not re.match(cls.ARN_PATTERN, value):
            if raise_error:
                raise ValidationError(error_message)
            return False

        return True

    @classmethod
    def arn(
            cls,
            value: Union[str, list],
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate if the given ARN(s) match the ARN pattern.
        :param value: The ARN(s) to be validated.
        :type value: str (or) list
        :param raise_error: Flag to raise an error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message to be used if raise_error is True and validation fails.
        :type custom_error_message: str
        :return: True if the ARN(s) match the pattern, False otherwise.
        :rtype: bool
        """
        _check_type(value, Union[str, list], True, 'value should be a string or list of strings.')
        _check_type(raise_error, Union[bool, None], True, 'raise_error should be a boolean.')
        _check_type(custom_error_message, Union[str, None], True, 'custom_error_message should be a boolean.')

        error_message = cls._get_error_message('arn', 'string or list of strings', custom_error_message)

        if not _check_type(value, Union[str, list], raise_error, error_message):
            return False

        if isinstance(value, str):
            return cls._arn(value, raise_error, error_message)
        elif isinstance(value, list):
            return all(cls._arn(val, raise_error, error_message) for val in value)


class PolicyValidator:
    """
    Validates AWS IAM policy documents.
    This class provides methods to validate various aspects of IAM policies.
    """
    # Regular expression pattern for validating version strings in policies.
    VERSION_PATTERN: str = r'(2008-10-17|2012-10-17)'
    # Regular expression pattern for validating effect strings in policies.
    EFFECT_PATTERN: str = r'(Allow|Deny)'
    # Regular expression pattern for validating principal strings in policies.
    PRINCIPAL_PATTERN: str = r'(AWS|Federated|Service|CanonicalUser)'

    @classmethod
    def _get_error_message(
            cls,
            variable_name: str,
            variable_type: str,
            custom_error_message: Optional[str] = None
    ) -> str:
        """
        Get the error message for the validation.
        :param variable_name: Name of the variable being validated.
        :type variable_name: str
        :param variable_type: Expected type of the variable.
        :type variable_type: str
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: Error message.
        :rtype: str
        """
        return custom_error_message or (
            f'{variable_name} should be of {variable_type}. Refer to '
            f'https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html '
            f'for more information.'
        )

    @classmethod
    def _version(
            cls,
            value: str,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate version string.
        :param value: The value to validate.
        :type value: str
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('version', 'string', custom_error_message)

        if not _check_type(value, str, raise_error, error_message) or not re.match(cls.VERSION_PATTERN, value):
            if raise_error:
                raise ValidationError(error_message)
            return False

        return True

    @classmethod
    def _id(
            cls,
            value: str,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate id string.
        :param value: The value to validate.
        :type value: str
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('id', 'string', custom_error_message)

        return _check_type(value, str, raise_error, error_message)

    @classmethod
    def _sid(
            cls,
            value: str,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate sid string.
        :param value: The value to validate.
        :type value: str
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('sid', 'string', custom_error_message)

        return _check_type(value, str, raise_error, error_message)

    @classmethod
    def _effect(
            cls,
            value: str,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate effect string.
        :param value: The value to validate.
        :type value: str
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('effect', 'string', custom_error_message)

        if not _check_type(value, str, raise_error, error_message) or not re.match(cls.EFFECT_PATTERN, value):
            if raise_error:
                raise ValidationError(error_message)
            return False

        return True

    @classmethod
    def _action(
            cls,
            value: Union[str, list],
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate action string or list of strings.
        :param value: The value to validate.
        :type value: str or list
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('action', 'string (*) or list of strings', custom_error_message)

        if not _check_type(value, Union[str, list], raise_error, error_message):
            return False

        if isinstance(value, str) and value != '*':
            if raise_error:
                raise ValidationError(error_message)
            return False
        elif isinstance(value, list):
            if len(value) == 0 or not all(_check_type(val, str, raise_error, error_message) for val in value):
                if raise_error:
                    raise ValidationError(error_message)
                return False

        return True

    @classmethod
    def _resource(
            cls,
            value: Union[str, list],
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate resource string or list of strings.
        :param value: The value to validate.
        :type value: str or list
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message(
            'resource', 'string (* or single value) or list of strings', custom_error_message
        )

        if not _check_type(value, Union[str, list], raise_error, error_message):
            return False

        if isinstance(value, list):
            if len(value) == 0 or not all(_check_type(val, str, raise_error, error_message) for val in value):
                if raise_error:
                    raise ValidationError(error_message)
                return False

        return True

    @classmethod
    def _principal(
            cls,
            value: Union[str, dict],
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate principal string or dictionary.
        :param value: The value to validate.
        :type value: str or dict
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('principal', 'string (*) or dictionary', custom_error_message)

        if not _check_type(value, Union[str, dict], raise_error, error_message):
            return False

        if isinstance(value, str) and value != '*':
            if raise_error:
                raise ValidationError(error_message)
            return False
        elif isinstance(value, dict):
            if len(value) == 0:
                if raise_error:
                    raise ValidationError(error_message)
                return False

            for p_key, p_values in value.items():
                if not _check_type(p_key, str, raise_error, error_message) \
                        or not re.match(cls.PRINCIPAL_PATTERN, p_key):
                    if raise_error:
                        raise ValidationError(error_message)
                    return False

                if len(p_values) == 0 or not _check_type(p_values, list, raise_error, error_message) \
                        or not all(_check_type(p_value, str, raise_error, error_message) for p_value in p_values):
                    if raise_error:
                        raise ValidationError(error_message)
                    return False

        return True

    @classmethod
    def _condition(
            cls,
            value: dict,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate condition dictionary.
        :param value: The value to validate.
        :type value: dict
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('condition', 'dictionary', custom_error_message)

        if not _check_type(value, dict, raise_error, error_message) or len(value) == 0:
            if raise_error:
                raise ValidationError(error_message)
            return False

        for c_map_key, c_map_values in value.items():
            if len(c_map_values) == 0 or not _check_type(c_map_key, str, raise_error, error_message) \
                    or not _check_type(c_map_values, dict, raise_error, error_message):
                if raise_error:
                    raise ValidationError(error_message)
                return False

            for c_type_key, c_type_values in c_map_values.items():
                if len(c_type_values) == 0 or not _check_type(c_type_key, str, raise_error, error_message) \
                        or not _check_type(c_type_values, Union[str, list, dict], raise_error, error_message):
                    if raise_error:
                        raise ValidationError(error_message)
                    return False

                if isinstance(c_type_values, list) \
                        and not all(_check_type(c_type_value, str, raise_error, error_message)
                                    for c_type_value in c_type_values):
                    return False
                elif isinstance(c_type_values, dict):
                    for c_key_key, c_key_values in c_type_values.items():
                        if len(c_key_values) == 0 or not _check_type(c_key_key, str, raise_error, error_message) \
                                or not _check_type(c_key_values, Union[str, list], raise_error, error_message):
                            if raise_error:
                                raise ValidationError(error_message)
                            return False

                        if isinstance(c_key_values, list) \
                                and (len(c_key_values) == 0
                                     or not all(_check_type(c_key_value, str, raise_error, error_message)
                                                for c_key_value in c_key_values)):
                            if raise_error:
                                raise ValidationError(error_message)
                            return False

        return True

    @classmethod
    def policy(
            cls,
            value: dict,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate policy dictionary.
        :param value: The value to validate.
        :type value: dict
        :param raise_error: Whether to raise error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: True if validation passes, False otherwise.
        :rtype: bool
        """
        _check_type(value, dict, True, 'value should be a dictionary.')
        _check_type(raise_error, Union[bool, None], True, 'raise_error should be a boolean.')
        _check_type(custom_error_message, Union[str, None], True, 'custom_error_message should be a string.')
        error_message = cls._get_error_message('policy', 'dictionary', custom_error_message)

        if not _check_type(value, dict, raise_error, error_message):
            return False

        if 'Statement' not in value.keys():
            if raise_error:
                raise ValidationError(error_message)
            return False

        for p_key, p_values in value.items():
            if len(p_values) == 0:
                if raise_error:
                    raise ValidationError(error_message)
                return False

            if p_key == 'Version':
                if not cls._version(p_values, raise_error, error_message):
                    return False
            elif p_key == 'Id':
                if not cls._id(p_values, raise_error, error_message):
                    return False
            elif p_key == 'Statement':
                statements = value.get('Statement', {})
                if 'Effect' not in statements.keys() or 'Action' not in statements.keys() \
                        or 'Resource' not in statements.keys():
                    if raise_error:
                        raise ValidationError(error_message)
                    return False

                if not cls._effect(statements.get('Effect', ''), raise_error, error_message) \
                        or not cls._action(statements.get('Action', ''), raise_error, error_message) \
                        or not cls._resource(statements.get('Resource', ''), raise_error, error_message):
                    return False

                for s_key, s_values in statements.items():
                    if len(s_values) == 0:
                        if raise_error:
                            raise ValidationError(error_message)
                        return False

                    if s_key == 'Sid':
                        if not cls._sid(s_values, raise_error, error_message):
                            return False
                    elif s_key in ['Principal', 'NotPrincipal']:
                        if not cls._principal(s_values, raise_error, error_message):
                            return False
                    elif s_key == 'Condition':
                        if not cls._condition(s_values, raise_error, error_message):
                            return False
                    elif s_key not in ['Effect', 'Action', 'Resource']:
                        if raise_error:
                            raise ValidationError(error_message)
                        return False
            elif p_key not in ['Version', 'Id', 'Statement']:
                if raise_error:
                    raise ValidationError(error_message)
                return False

        return True


class TagValidator:
    """
    Validates tags according to predefined patterns.
    This class provides methods to validate keys and values of tags in dictionaries or lists of dictionaries.
    """
    # This regular expression pattern is used to validate keys in a dictionary of tags.
    KEY_PATTERN: str = r'^[a-zA-Z0-9\.\-_:]{1,128}$'
    # This regular expression pattern is used to validate values in a dictionary of tags.
    VALUE_PATTERN: str = r'^[a-zA-Z0-9\.\-_:]{1,128}?$'

    @classmethod
    def _get_error_message(
            cls,
            variable_name: str,
            variable_type: str,
            custom_error_message: Optional[str] = None
    ) -> str:
        """
        Get the error message for the validation.
        :param variable_name: Name of the variable being validated.
        :type variable_name: str
        :param variable_type: Expected type of the variable.
        :type variable_type: str
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :return: Error message.
        :rtype: str
        """
        return custom_error_message or (
            f'{variable_name} should be of {variable_type}. Refer to '
            f'https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html '
            f'for more information.'
        )

    @classmethod
    def _tag(
            cls,
            value: dict,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate a dictionary of tags.
        :param value: The dictionary of tags to validate.
        :type value: dict
        :param raise_error: Flag indicating whether to raise an error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message to use if validation fails.
        :type custom_error_message: str
        :return: True if the dictionary of tags is valid, False otherwise.
        :rtype: bool
        """
        error_message = cls._get_error_message('tag', 'dictionary', custom_error_message)

        key_pattern = re.compile(cls.KEY_PATTERN)
        value_pattern = re.compile(cls.VALUE_PATTERN)

        if not _check_type(value, dict, raise_error, error_message):
            return False

        for key, val in value.items():
            if not _check_type(key, str, raise_error, error_message) \
                    or not _check_type(val, str, raise_error, error_message) \
                    or not key_pattern.match(key) or not value_pattern.match(val):
                if raise_error:
                    raise ValidationError(error_message)
                return False

        return True

    @classmethod
    def tag(
            cls,
            value: Union[dict, list],
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate a dictionary or a list of dictionaries of tags.
        :param value: The value to validate, either a dictionary or a list of dictionaries.
        :type value: dict or list
        :param raise_error: Flag indicating whether to raise an error if validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message to use if validation fails.
        :type custom_error_message: str
        :return: True if the value is valid, False otherwise.
        :rtype: bool
        """
        _check_type(value, Union[dict, list], True, 'value should be a dictionary or list.')
        _check_type(raise_error, Union[bool, None], True, 'raise_error should be a boolean.')
        _check_type(custom_error_message, Union[str, None], True, 'custom_error_message should be a boolean.')

        error_message = cls._get_error_message('tag', 'dictionary or list of dictionaries', custom_error_message)

        if not _check_type(value, Union[dict, list], raise_error, error_message):
            return False

        if isinstance(value, dict):
            return cls._tag(value, raise_error, error_message)
        elif isinstance(value, list):
            return all(cls._tag(val, raise_error, error_message) for val in value)


class Validator:
    """
    Validates according to predefined patterns.
    This class provides methods to validate various aspects of AWS, such as region code.
    """
    # Regular expression pattern used to validate region codes.
    REGION_PATTERN: str = r'^[a-z]{2}-[a-z]{4,}-\d$'

    @classmethod
    def _get_error_message(
            cls,
            variable_name: str,
            variable_type: str,
            custom_error_message: Optional[str] = None,
            reference_link: Optional[str] = None
    ) -> str:
        """
        Get the error message for the validation.
        :param variable_name: Name of the variable being validated.
        :type variable_name: str
        :param variable_type: Expected type of the variable.
        :type variable_type: str
        :param custom_error_message: Custom error message, if provided.
        :type custom_error_message: str
        :param reference_link: Reference link, if provided.
        :type reference_link: str
        :return: Error message.
        :rtype: str
        """
        return custom_error_message or (
            f'{variable_name} should be of {variable_type}.'
            f'{f"Refer to {reference_link} for more information." if reference_link else ""}'
        )

    @classmethod
    def region(
            cls,
            value: str,
            raise_error: Optional[bool] = True,
            custom_error_message: Optional[str] = None
    ) -> bool:
        """
        Validate a region value.
        :param value: The region value to be validated.
        :type value: str
        :param raise_error: Flag indicating whether to raise an error when validation fails.
        :type raise_error: bool
        :param custom_error_message: Custom error message to be used if validation fails.
        :type custom_error_message: str
        :return: True if the region value is valid, False otherwise.
        :rtype: bool
        """
        _check_type(value, str, True, 'value should be a string.')
        _check_type(raise_error, Union[bool, None], True, 'raise_error should be a boolean.')
        _check_type(custom_error_message, Union[str, None], True, 'custom_error_message should be a string.')
        error_message = cls._get_error_message(
            'region',
            'string',
            custom_error_message,
            'https://docs.aws.amazon.com/organizations/latest/APIReference/API_DescribeAccount.html'
        )

        if not _check_type(value, str, raise_error, error_message) or not re.match(cls.REGION_PATTERN, value):
            if raise_error:
                raise ValidationError(error_message)
            return False

        return True
