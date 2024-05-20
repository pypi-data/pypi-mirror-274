__all__ = [
    "Account",
    "Credentials",
    "Session",
    "advsearch",
    "exceptions",
    "models",
    "validators"
]
__name__ = "pyawsopstoolkit"
__version__ = "0.1.5"
__description__ = """
This extensive package, AWS Ops Toolkit, offers a wide range of features and enhancements designed to streamline
and optimize interactions with Amazon Web Services (AWS). As of now, the toolkit includes a robust set of
functionalities including validators for ensuring the correctness of AWS ARNs, IAM policy formats, and more.
Furthermore, it provides session management classes tailored for seamless integration within the application
ecosystem, complete with a versatile assume role function.

As we continue to evolve, watch this space for upcoming additions and enhancements, promising even greater utility
and efficiency in AWS-related workflows.
"""

from pyawsopstoolkit.__main__ import Credentials, Account, Session
