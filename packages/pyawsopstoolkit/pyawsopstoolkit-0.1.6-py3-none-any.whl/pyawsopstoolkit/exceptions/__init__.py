__all__ = [
    "AssumeRoleError",
    "SearchAttributeError",
    "ValidationError"
]
__name__ = "pyawsopstoolkit.exceptions"
__description__ = """
This package offers a collection of exception classes tailored for handling errors within the AWS Ops Toolkit.
These exceptions are specifically designed to address different scenarios and errors that may occur during the
execution of pyawsopstoolkit operations, providing comprehensive support for error handling and debugging within
the toolkit.
"""

from pyawsopstoolkit.exceptions.__main__ import AssumeRoleError, ValidationError, SearchAttributeError
