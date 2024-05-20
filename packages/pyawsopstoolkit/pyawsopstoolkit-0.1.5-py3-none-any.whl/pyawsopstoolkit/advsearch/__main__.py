import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any

import pyawsopstoolkit.models
from pyawsopstoolkit.__interfaces__ import IAccount, ISession
from pyawsopstoolkit.__validations__ import Validation

MAX_WORKERS = 10

# This module supports various conditions for advanced searches, outlined below as global constants.
OR: str = 'OR'  # Represents the "or" condition
AND: str = 'AND'  # Represents the "and" condition

LESS_THAN: str = 'lt'  # Represents the less than ("<") value
LESS_THAN_OR_EQUAL_TO: str = 'lte'  # Represents the less than or equal to ("<=") value
GREATER_THAN: str = 'gt'  # Represents the greater than (">") value
GREATER_THAN_OR_EQUAL_TO: str = 'gte'  # Represents the greater than or equal to (">=") value
EQUAL_TO: str = 'eq'  # Represents the equal to ("=") value
NOT_EQUAL_TO: str = 'ne'  # Represents the not equal to ("!=") value
BETWEEN: str = 'between'  # Represents the between range ("< x <") value


def _match_condition(value: str, role_field: str, condition: str, matched: bool) -> bool:
    """
    Matches the condition based on the specified parameters.
    :param value: The value to be evaluated.
    :type value: str
    :param role_field: The value to compare against.
    :type role_field: str
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    if not value or not role_field:
        return False

    if re.search(value, role_field, re.IGNORECASE):
        if condition == OR:
            return True
    elif condition == AND:
        return False

    return matched


def _match_compare_condition(value: dict, role_field: Any, condition: str, matched: bool) -> bool:
    """
    Matches the condition by comparing based on the specified parameters.
    :param value: The value to be evaluated.
    :type value: dict
    :param role_field: The value to compare against.
    :type role_field: Any
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    match = True
    if isinstance(value, dict):
        for operator, compare_value in value.items():
            if isinstance(role_field, datetime) and isinstance(compare_value, str):
                compare_value = datetime.fromisoformat(compare_value).replace(tzinfo=None)

            if operator == LESS_THAN and not role_field < compare_value:
                match = False
            elif operator == LESS_THAN_OR_EQUAL_TO and not role_field <= compare_value:
                match = False
            elif operator == EQUAL_TO and not role_field == compare_value:
                match = False
            elif operator == NOT_EQUAL_TO and not role_field != compare_value:
                match = False
            elif operator == GREATER_THAN and not role_field > compare_value:
                match = False
            elif operator == GREATER_THAN_OR_EQUAL_TO and not role_field >= compare_value:
                match = False
            elif operator == BETWEEN:
                if not isinstance(compare_value, list) or len(compare_value) != 2:
                    raise ValueError('The "between" operator requires a list of two values.')
                if isinstance(role_field, datetime):
                    compare_value[0] = datetime.fromisoformat(compare_value[0]).replace(tzinfo=None)
                    compare_value[1] = datetime.fromisoformat(compare_value[1]).replace(tzinfo=None)
                if not (compare_value[0] <= role_field <= compare_value[1]):
                    match = False
    else:
        raise ValueError('Conditions should be specified as a dictionary with operators.')

    if condition == OR and match:
        return True
    elif condition == AND and not match:
        return False

    return matched


def _match_tag_condition(value, tags, condition: str, matched: bool, key_only: bool) -> bool:
    """
    Matches the condition based on the specified tags.
    :param value: The value to be evaluated.
    :type value: Any
    :param tags: The value to compare against.
    :type tags: Any
    :param condition: The condition to be applied: 'OR' or 'AND'.
    :type condition: str
    :param matched: The current matching status.
    :type matched: bool
    :param key_only: Flag to indicate to match just key or both key and value.
    :type key_only: bool
    :return: Returns a boolean value (True or False) based on the comparison.
    :rtype: bool
    """
    match = False
    if key_only:
        if value in tags:
            match = True
    else:
        match = True
        for key, val in value.items():
            if tags.get(key) != val:
                match = False
                break

    if not matched:
        return False

    if condition == "OR":
        return match
    elif condition == "AND":
        return match
    else:
        return matched


class IAM:
    """
    A class encapsulating advanced IAM-related search functionalities, facilitating the exploration of roles,
    users, and more.
    """

    def __init__(
            self,
            session: ISession
    ) -> None:
        """
        Initializes the constructor of the IAM class.
        :param session: An ISession object providing access to AWS services.
        :type session: ISession
        """
        Validation.validate_type(session, ISession, 'session should be of ISession type.')

        self._session = session

    @property
    def session(self) -> ISession:
        """
        Gets the ISession object which provides access to AWS services.
        :return: The ISession object which provide access to AWS services.
        :rtype: ISession
        """
        return self._session

    @session.setter
    def session(self, value: ISession) -> None:
        """
        Sets the ISession object which provides access to AWS services.
        :param value: The ISession object which provides access to AWS services.
        :type value: ISession
        """
        Validation.validate_type(value, ISession, 'session should be of ISession type.')

        self._session = value

    def _list_roles(self) -> list:
        """
        Utilizing boto3 IAM, this method retrieves a list of all roles leveraging the provided ISession object.
        Note: The returned dictionary excludes PermissionsBoundary, LastUsed, and Tags. For further details,
        please consult the official documentation:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/list_roles.html.
        :return: A list containing IAM roles.
        :rtype: list
        """
        roles_to_process = []

        from botocore.exceptions import ClientError
        try:
            iam_client = self.session.get_session().client('iam')
            iam_paginator = iam_client.get_paginator('list_roles')

            for page in iam_paginator.paginate():
                roles_to_process.extend(page.get('Roles', []))
        except ClientError as e:
            raise e

        return roles_to_process

    def _get_role(self, role_name: str) -> dict:
        """
        Utilizing boto3 IAM, this method retrieves comprehensive details of an IAM role identified by the
        specified role name.
        :return: Details of the IAM role.
        :rtype: dict
        """
        from botocore.exceptions import ClientError
        try:
            iam_client = self.session.get_session().client('iam')
            return iam_client.get_role(RoleName=role_name)
        except ClientError as e:
            raise e

    @staticmethod
    def _convert_to_iam_role(account: IAccount, role: dict) -> pyawsopstoolkit.models.IAMRole:
        """
        This function transforms the dictionary response from boto3 IAM into a format compatible with the
        AWS Ops Toolkit, adhering to the pyawsopstoolkit.models structure. Additionally, it incorporates
        account-related summary information into the IAM role details.
        :param account: An IAccount object containing AWS account information.
        :type account: IAccount
        :param role: The boto3 IAM service response for an IAM role.
        :type role: dict
        :return: An AWS Ops Toolkit compatible object containing all IAM role details.
        :rtype: IAMRole
        """
        iam_role = pyawsopstoolkit.models.IAMRole(
            account=account,
            name=role.get('RoleName', ''),
            id=role.get('RoleId', ''),
            arn=role.get('Arn', ''),
            max_session_duration=role.get('MaxSessionDuration', 0),
            path=role.get('Path', ''),
            created_date=role.get('CreateDate', None),
            assume_role_policy_document=role.get('AssumeRolePolicyDocument', None),
            description=role.get('Description', None)
        )

        _permissions_boundary = role.get('PermissionsBoundary', {})
        if _permissions_boundary:
            boundary = pyawsopstoolkit.models.IAMRolePermissionsBoundary(
                type=_permissions_boundary.get('PermissionsBoundaryType', ''),
                arn=_permissions_boundary.get('PermissionsBoundaryArn', '')
            )
            iam_role.permissions_boundary = boundary

        _last_used = role.get('RoleLastUsed', {})
        if _last_used:
            last_used = pyawsopstoolkit.models.IAMRoleLastUsed(
                used_date=_last_used.get('LastUsedDate', None),
                region=_last_used.get('Region', None)
            )
            iam_role.last_used = last_used

        _tags = role.get('Tags', [])
        if _tags:
            iam_role.tags = _tags

        return iam_role

    def search_roles(
            self,
            condition: str = OR,
            include_details: bool = False,
            **kwargs
    ) -> list[pyawsopstoolkit.models.IAMRole]:
        """
        Returns a list of IAM roles using advanced search features supported by the specified arguments.
        For details on supported kwargs, please refer to the readme document.
        :param condition: The condition to be applied: 'OR' or 'AND'.
        :type condition: str
        :param include_details: Flag to indicate to include additional details of the IAM role.
        This includes information about permissions boundary, last used, and tags. Default is False.
        :type include_details: bool
        :param kwargs: Key-based arguments defining search criteria.
        :return: A list of IAM roles.
        :rtype: list
        """

        def _process_role(role_detail):
            if include_details:
                role_detail = self._get_role(role_detail.get('RoleName', '')).get('Role', {})

            return self._convert_to_iam_role(self.session.get_account(), role_detail)

        def _match_role(role_detail):
            if role_detail:
                matched = False if condition == OR else True
                for key, value in kwargs.items():
                    if value is not None:
                        role_field = ''
                        if key.lower() == 'path':
                            role_field = role_detail.get('Path', '')
                        elif key.lower() == 'name':
                            role_field = role_detail.get('RoleName', '')
                        elif key.lower() == 'id':
                            role_field = role_detail.get('RoleId', '')
                        elif key.lower() == 'arn':
                            role_field = role_detail.get('Arn', '')
                        elif key.lower() == 'description':
                            role_field = role_detail.get('Description', '')
                        elif key.lower() == 'permissions_boundary_type':
                            if include_details:
                                role_detail = self._get_role(role_detail.get('RoleName', '')).get('Role', {})
                                _permissions_boundary = role_detail.get('PermissionsBoundary', {})
                                role_field = _permissions_boundary.get('PermissionsBoundaryType', '')
                        elif key.lower() == 'permissions_boundary_arn':
                            if include_details:
                                role_detail = self._get_role(role_detail.get('RoleName', '')).get('Role', {})
                                _permissions_boundary = role_detail.get('PermissionsBoundary', {})
                                role_field = _permissions_boundary.get('PermissionsBoundaryArn', '')
                        elif key.lower() == 'max_session_duration':
                            role_field = role_detail.get('MaxSessionDuration', 0)
                            matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'created_date':
                            role_field = role_detail.get('CreateDate', None)
                            if isinstance(role_field, datetime):
                                role_field = role_field.replace(tzinfo=None)
                                matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'last_used_date':
                            if include_details:
                                role_detail = self._get_role(role_detail.get('RoleName', '')).get('Role', {})
                                _last_used = role_detail.get('RoleLastUsed', {})
                                role_field = _last_used.get('LastUsedDate', None)
                                if isinstance(role_field, datetime):
                                    role_field = role_field.replace(tzinfo=None)
                                    matched = _match_compare_condition(value, role_field, condition, matched)
                        elif key.lower() == 'last_used_region':
                            if include_details:
                                role_detail = self._get_role(role_detail.get('RoleName', '')).get('Role', {})
                                _last_used = role_detail.get('RoleLastUsed', {})
                                role_field = _last_used.get('Region', '')
                        elif key.lower() == 'tag_key':
                            if include_details:
                                role_detail = self._get_role(role_detail.get('RoleName', '')).get('Role', {})
                                tags = {tag['Key']: tag['Value'] for tag in role_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=True)
                        elif key.lower() == 'tag':
                            if include_details:
                                role_detail = self._get_role(role_detail.get('RoleName', '')).get('Role', {})
                                tags = {tag['Key']: tag['Value'] for tag in role_detail.get('Tags', [])}
                                matched = _match_tag_condition(value, tags, condition, matched, key_only=False)

                        if key.lower() not in [
                            'max_session_duration', 'created_date', 'last_used_date', 'tag_key', 'tag'
                        ]:
                            matched = _match_condition(value, role_field, condition, matched)

                        if (condition == OR and matched) or (condition == AND and not matched):
                            break

                if matched:
                    return _process_role(role_detail)

        roles_to_return = []

        from botocore.exceptions import ClientError
        try:
            include_details_keys = {
                'permissions_boundary_type', 'permissions_boundary_arn', 'last_used_date', 'last_used_region',
                'tag', 'tag_key'
            }

            if not include_details and any(k in include_details_keys for k in kwargs):
                from pyawsopstoolkit.exceptions import SearchAttributeError
                raise SearchAttributeError(
                    'include_details is required for below keys: permissions_boundary_type, '
                    'permissions_boundary_arn, last_used_date, last_used_region, tag, tag_key.'
                )

            roles_to_process = self._list_roles()

            if len(kwargs) == 0:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_role = {executor.submit(_process_role, role): role for role in roles_to_process}
                    for future in as_completed(future_to_role):
                        role_result = future.result()
                        if role_result is not None:
                            roles_to_return.append(role_result)

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                future_to_role = {executor.submit(_match_role, role): role for role in roles_to_process}
                for future in as_completed(future_to_role):
                    role_result = future.result()
                    if role_result is not None:
                        roles_to_return.append(role_result)
        except ClientError as e:
            raise e

        return roles_to_return
