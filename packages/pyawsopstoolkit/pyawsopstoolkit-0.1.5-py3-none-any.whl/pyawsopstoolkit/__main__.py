from datetime import datetime
from typing import Optional, Union

from pyawsopstoolkit.__interfaces__ import ICredentials, IAccount, ISession
from pyawsopstoolkit.__validations__ import Validation
from pyawsopstoolkit.exceptions import AssumeRoleError
from pyawsopstoolkit.validators import ArnValidator, PolicyValidator, TagValidator, AccountValidator, Validator


class Credentials(ICredentials):
    """
    Represents a set of credentials including an access key, secret access key, token, and optional expiry datetime.
    :param access_key: Access key string.
    :type access_key: str
    :param secret_access_key: Secret access key string.
    :type secret_access_key: str
    :param token: Token string.
    :type token: str
    :param expiry: Optional expiry datetime. Defaults to None.
    :type expiry: datetime
    """

    def __init__(
            self,
            access_key: str,
            secret_access_key: str,
            token: Optional[str] = None,
            expiry: Optional[datetime] = None
    ) -> None:
        """
        Initialize Credentials object.
        :param access_key: Access key string.
        :type access_key: str
        :param secret_access_key: Secret access key string.
        :type secret_access_key: str
        :param token: Token string.
        :type token: str
        :param expiry: Optional expiry datetime.
        :type expiry: datetime
        """
        Validation.validate_type(access_key, str, 'access_key should be a string.')
        Validation.validate_type(secret_access_key, str, 'secret_access_key should be a string.')
        Validation.validate_type(token, Union[str, None], 'token should be a string.')
        Validation.validate_type(expiry, Union[datetime, None], 'expiry should be a datetime.')

        self._access_key = access_key
        self._secret_access_key = secret_access_key
        self._token = token
        self._expiry = expiry

    @property
    def access_key(self) -> str:
        """
        Get access key.
        :return: Access key string.
        :rtype: str
        """
        return self._access_key

    @access_key.setter
    def access_key(self, value: str) -> None:
        """
        Set access key.
        :param value: New access key.
        :type value: str
        """
        Validation.validate_type(value, str, 'access_key should be a string.')
        self._access_key = value

    @property
    def secret_access_key(self) -> str:
        """
        Get secret access key.
        :return: Secret access key string.
        :rtype: str
        """
        return self._secret_access_key

    @secret_access_key.setter
    def secret_access_key(self, value: str) -> None:
        """
        Set secret access key.
        :param value: New secret access key.
        :type value: str
        """
        Validation.validate_type(value, str, 'secret_access_key should be a string.')
        self._secret_access_key = value

    @property
    def token(self) -> str:
        """
        Get token.
        :return: Token string.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        """
        Set token.
        :param value: New token.
        :type value: str
        """
        Validation.validate_type(value, str, 'token should be a string.')
        self._token = value

    @property
    def expiry(self) -> Optional[datetime]:
        """
        Get expiry datetime.
        :return: Expiry datetime.
        :rtype: datetime
        """
        return self._expiry

    @expiry.setter
    def expiry(self, value: Optional[datetime] = None) -> None:
        """
        Set expiry datetime.
        :param value: New expiry datetime.
        :type value: datetime
        """
        Validation.validate_type(value, Union[datetime, None], 'expiry should be a datetime.')
        self._expiry = value

    def __str__(self) -> str:
        """
        Convert Credentials object to string.
        :return: String representation of Credentials object.
        :rtype: str
        """
        access_key = f'"{self.access_key}"'
        secret_access_key = f'"{self.secret_access_key}"'
        token = f'"{self.token}"' if self.token else None
        expiry = f'{self.expiry.isoformat()}' if self.expiry else None

        return (
            f'Credentials('
            f'access_key={access_key},'
            f'secret_access_key={secret_access_key},'
            f'token={token},'
            f'expiry={expiry}'
            f')'
        )

    def __dict__(self) -> dict:
        """
        Convert Credentials object to dictionary.
        :return: Dictionary representation of Credentials object.
        :rtype: dict
        """
        return {
            "access_key": self.access_key,
            "secret_access_key": self.secret_access_key,
            "token": self.token if self.token else None,
            "expiry": self.expiry.isoformat() if self.expiry else None
        }


class Account(IAccount):
    """
    Represents an AWS account with various attributes. This class implements the IAccount interface, providing basic
    functionality for managing an AWS account.
    """

    def __init__(self, number: str) -> None:
        """
        Initializes an Account object with a given account number.
        :param number: The account number to be set.
        :type number: str
        """
        AccountValidator.number(number)

        self._number = number

    @property
    def number(self) -> str:
        """
        Getter method to retrieve the account number.
        :return: The account number.
        :rtype: str
        """
        return self._number

    @number.setter
    def number(self, value: str) -> None:
        """
        Setter method to set the account number.
        :param value: The account number to be set.
        :type value: str
        """
        AccountValidator.number(value)
        self._number = value

    def __str__(self) -> str:
        """
        Return a string representation of the Account object.
        :return: String representation of the IAMRole object.
        :rtype: str
        """
        return (
            f'Account('
            f'number="{self.number}"'
            f')'
        )

    def __dict__(self) -> dict:
        """
        Return a dictionary representation of the Account object.
        :return: Dictionary representation of the Account object.
        :rtype: dict
        """
        return {
            "number": self.number
        }


class Session(ISession):
    """
    This class represents a boto3 Session with various attributes. It implements the ISession interface, offering
    functionality to manage sessions. Additionally, it provides the option to assume a session.
    """

    def __init__(
            self,
            profile_name: Optional[str] = None,
            credentials: Optional[ICredentials] = None,
            region_code: Optional[str] = 'eu-west-1'
    ) -> None:
        """
        Initializes a Session object for AWS.
        :param profile_name: The name of the AWS profile to be used for authentication.
        :type profile_name: str
        :param credentials: An object containing AWS credentials, including access key, secret access key, and token.
        :type credentials: Credentials
        :param region_code: The code representing the AWS region to operate in, e.g., "eu-west-1".
        :type region_code: str
        """
        if (profile_name is not None) == (credentials is not None):
            raise ValueError('Either profile_name or credentials should be provided, but not both.')

        if profile_name:
            Validation.validate_type(profile_name, str, 'profile_name should be a string.')
            self._profile_name = profile_name
            self._credentials = None
        elif credentials:
            Validation.validate_type(credentials, Credentials, 'credentials should be of Credentials type.')
            self._profile_name = None
            self._credentials = credentials
        else:
            raise ValueError('At least profile_name or credentials is required.')

        Validator.region(region_code)
        self._region_code = region_code

    @property
    def profile_name(self) -> str:
        """
        Getter for the profile name.
        :return: The name of the AWS profile.
        :rtype: str
        """
        return self._profile_name

    @profile_name.setter
    def profile_name(self, value: Optional[str] = None) -> None:
        """
        Setter for updating the profile name.
        :param value: The new name of the AWS profile.
        :type value: str
        """
        if self.credentials is not None:
            raise ValueError('Either profile_name or credentials should be provided, but not both.')

        Validation.validate_type(value, str, 'profile_name should be a string.')
        self._profile_name = value

    @property
    def credentials(self) -> ICredentials:
        """
        Getter for the AWS credentials.
        :return: Credentials object for AWS.
        :rtype: Credentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, value: Optional[ICredentials] = None) -> None:
        """
        Setter for updating the AWS credentials.
        :param value: The new AWS credentials object to be set.
        :type value: Credentials
        """
        if self.profile_name is not None:
            raise ValueError('Either profile_name or credentials should be provided, but not both.')

        Validation.validate_type(value, Credentials, 'credentials should be of Credentials type.')
        self._credentials = value

    @property
    def region_code(self) -> str:
        """
        Getter for the region code.
        :return: The region code.
        :rtype: str
        """
        return self._region_code

    @region_code.setter
    def region_code(self, value: Optional[str] = 'eu-west-1') -> None:
        """
        Setter for updating the region code.
        :param value: The new region code to be set.
        :type value: str
        """
        Validator.region(value)
        self._region_code = value

    def get_session(self):
        """
        Returns the boto3.Session object based on the specified parameters within the class object.
        Priority is given to profile_name, followed by credentials.
        This method performs a quick S3 list buckets action to verify if the session is valid.
        :return: The boto3 Session object based on the specified parameters within the class object.
        :rtype: boto3.Session
        """
        import boto3

        from botocore.exceptions import ClientError, ProfileNotFound

        session = None
        try:
            if self.profile_name:
                session = boto3.Session(profile_name=self.profile_name)
            elif self.credentials:
                session = boto3.Session(
                    aws_access_key_id=self.credentials.access_key,
                    aws_secret_access_key=self.credentials.secret_access_key,
                    aws_session_token=self.credentials.token
                )
            else:
                raise ValueError('At least profile_name or credentials is required.')

            session.client('s3').list_buckets()
        except ProfileNotFound:
            raise ValueError(f'Profile "{self.profile_name}" not found.')
        except ClientError as e:
            if e.response['Error']['Code'] != 'AccessDenied':
                raise ValueError(f'Failed to create session: {e}.')

        return session

    def get_config(self):
        """
        Returns the botocore.config.Config based on the specified region code within the class object.
        :return: The botocore Config object based on the specified region code within the class object.
        :rtype: botocore.config.Config
        """
        from botocore.config import Config

        return Config(region_name=self.region_code)

    def get_account(self) -> IAccount:
        """
        Returns the AWS account number based on the get_session with specified parameters within the class object.
        :return: The AWS account number.
        :rtype: Account
        """
        from botocore.exceptions import ClientError

        session = self.get_session()
        try:
            account_id = session.client('sts').get_caller_identity().get('Account', '')
            if account_id:
                return Account(account_id)
        except ClientError as e:
            raise ValueError(f'Failed to retrieve AWS account number: {e}.')

    def get_credentials_for_profile(self) -> ICredentials:
        """
        Returns the AWS credentials, i.e., access key, secret access key, and token based on the get_session with
        specified parameters within the class object.
        :return: The AWS credentials.
        :rtype: Credentials
        """
        from botocore.exceptions import ClientError, ProfileNotFound

        if self.profile_name is None:
            raise ValueError('profile_name is not set.')

        session = self.get_session()
        try:
            creds = session.get_credentials()
            return Credentials(
                access_key=creds.access_key,
                secret_access_key=creds.secret_key,
                token=creds.token
            )
        except ProfileNotFound:
            raise ValueError(f'Profile "{self.profile_name}" not found.')
        except ClientError as e:
            raise ValueError(f'Failed to retrieve AWS credentials: {e}.')

    def assume_role(
            self,
            role_arn: str,
            role_session_name: Optional[str] = 'AssumeSession',
            policy_arns: Optional[list] = None,
            policy: Optional[Union[str, dict]] = None,
            duration_seconds: Optional[int] = 3600,
            tags: Optional[list] = None
    ):
        """
        Returns the boto3.Session object for the assumed role based on the specified parameters.
        :param role_arn: The AWS ARN of the role to be assumed.
        :type role_arn: str
        :param role_session_name: Optional, The name for the AWS assumed session. Default is considered
        as 'AssumeSession'.
        :type role_session_name: str
        :param policy_arns: Optional, The list of IAM policy ARNs to attach to the assumed role session.
        :type policy_arns: list
        :param policy: Optional, The policy to be attached to the assumed role session.
        :type policy: str or dict
        :param duration_seconds: Optional, The duration (in seconds) to be set to the assumed role session.
        Default is considered as 3600 seconds.
        :type duration_seconds: int
        :param tags: Optional, The tags to be applied to the assumed role session.
        :type tags: dict
        :return: The Session object of the assumed role session.
        :rtype: ISession
        """
        from botocore.exceptions import ClientError

        ArnValidator.arn(role_arn)
        Validation.validate_type(role_session_name, Union[str, None], 'role_session_name should be a string.')
        Validation.validate_type(policy_arns, Union[list, None], 'policy_arns should be list of strings.')
        if policy_arns:
            ArnValidator.arn(policy_arns)
        if policy:
            PolicyValidator.policy(policy)
        Validation.validate_type(duration_seconds, Union[int, None], 'duration_seconds should be an integer.')
        if tags:
            TagValidator.tag(tags)

        session = self.get_session()
        try:
            sts_client = session.client('sts')
            params = {
                "RoleArn": role_arn,
                "RoleSessionName": role_session_name,
                "DurationSeconds": duration_seconds
            }
            if policy_arns:
                params.update({
                    "PolicyArns": policy_arns
                })
            if policy:
                params.update({
                    "Policy": policy
                })
            if tags:
                params.update({
                    "Tags": tags
                })
            response = sts_client.assume_role(**params)
            if response:
                creds = response.get('Credentials', {})
                if creds:
                    return Session(credentials=Credentials(
                        access_key=creds.get('AccessKeyId', ''),
                        secret_access_key=creds.get('SecretAccessKey', ''),
                        token=creds.get('SessionToken', ''),
                        expiry=creds.get('Expiration', datetime.utcnow())
                    ))
        except ClientError as e:
            raise AssumeRoleError(role_arn=role_arn, exception=e)
