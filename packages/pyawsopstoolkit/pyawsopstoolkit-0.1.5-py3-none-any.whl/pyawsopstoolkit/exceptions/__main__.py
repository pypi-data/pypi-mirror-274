from typing import Optional, Union

from pyawsopstoolkit.__validations__ import Validation


class AssumeRoleError(Exception):
    """
    Custom exception class designed for AWS Ops Toolkit.
    This exception is typically raised when there's a failure during the assumption of a role session.
    """

    def __init__(
            self,
            role_arn: str,
            exception: Optional[Exception] = None
    ) -> None:
        """
        Constructor for the AssumeRoleError class.
        :param role_arn: The Amazon Resource Name (ARN) of the role.
        :type role_arn: str
        :param exception: The exception that occurred, if any.
        :type exception: Exception
        """
        Validation.validate_type(role_arn, str, 'role_arn should be a string.')
        Validation.validate_type(exception, Union[Exception, None], 'exception should be of Exception type.')

        self._role_arn = role_arn
        self._exception = exception
        self._message = f'ERROR: Unable to assume role "{role_arn}".{f" {exception}." if exception else ""}'
        super().__init__(self._message)

    @property
    def exception(self) -> Optional[Exception]:
        """
        Getter for exception attribute.
        :return: The exception that occurred, if any.
        :rtype: Exception
        """
        return self._exception

    @property
    def message(self) -> str:
        """
        Getter for message attribute.
        :return: The error message.
        :rtype: str
        """
        return self._message

    @property
    def role_arn(self) -> str:
        """
        Getter for role_arn attribute.
        :return: The Amazon Resource Name (ARN) of the role.
        :rtype: str
        """
        return self._role_arn


class SearchAttributeError(AttributeError):
    """
    Custom exception class for AWS Ops Toolkit.
    This exception is typically raised when either invalid attributes are provided or key attributes are missing.
    """

    def __init__(
            self,
            message: str,
            exception: Optional[Exception] = None
    ) -> None:
        """
        Constructor for the SearchAttributeError class.
        :param message: The error message.
        :type message: str
        :param exception: The exception that occurred, if any.
        :type exception: Exception
        """
        Validation.validate_type(message, str, 'message should be a string.')
        Validation.validate_type(exception, Union[Exception, None], 'exception should be of Exception type.')

        self._exception = exception
        self._message = f'ERROR: {message}.{f" {exception}." if exception else ""}'
        super().__init__(self._message)

    @property
    def exception(self) -> Optional[Exception]:
        """
        Getter for exception attribute.
        :return: The exception that occurred, if any.
        :rtype: Exception
        """
        return self._exception

    @property
    def message(self) -> str:
        """
        Getter for message attribute.
        :return: The error message.
        :rtype: str
        """
        return self._message


class ValidationError(Exception):
    """
    Custom exception class for AWS Ops Toolkit.
    This exception is typically raised when validation fails.
    """

    def __init__(
            self,
            message: str,
            exception: Optional[Exception] = None
    ) -> None:
        """
        Constructor for the ValidationError class.
        :param message: The error message.
        :type message: str
        :param exception: The exception that occurred, if any.
        :type exception: Exception
        """
        Validation.validate_type(message, str, 'message should be a string.')
        Validation.validate_type(exception, Union[Exception, None], 'exception should be of Exception type.')

        self._exception = exception
        self._message = f'ERROR: {message}.{f" {exception}." if exception else ""}'
        super().__init__(self._message)

    @property
    def exception(self) -> Optional[Exception]:
        """
        Getter for exception attribute.
        :return: The exception that occurred, if any.
        :rtype: Exception
        """
        return self._exception

    @property
    def message(self) -> str:
        """
        Getter for message attribute.
        :return: The error message.
        :rtype: str
        """
        return self._message
