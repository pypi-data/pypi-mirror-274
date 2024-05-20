import pyawsopstoolkit.models
from pyawsopstoolkit.__interfaces__ import ISession
from pyawsopstoolkit.__validations__ import Validation


class IAM:
    """
    A class encapsulating security risks and vulnerabilities associated with the IAM service.
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
        Validation.validate_type(session, ISession, 'session should be of Session type.')

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
        Validation.validate_type(value, ISession, 'session should be of Session type.')

        self._session = value

    def roles_without_permissions_boundary(self) -> list[pyawsopstoolkit.models.IAMRole]:
        """
        Returns a list of IAM roles that do not have an associated permissions boundary.
        :return: A list of IAM roles without an associated permissions boundary.
        :rtype: list
        """
        from pyawsopstoolkit import advsearch
        iam_object = advsearch.IAM(self.session)
        iam_roles = iam_object.search_roles(include_details=True)

        if iam_roles is None:
            return []

        return [
            role for role in iam_roles
            if role.permissions_boundary is None and role.path != '/aws-service-role/'
        ]
