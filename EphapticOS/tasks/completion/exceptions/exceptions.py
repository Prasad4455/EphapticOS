from fastapi import status

from EphapticOS.exceptions import EphapticOSValidationError


class NoRelevantDataError(EphapticOSValidationError):
    """
    Represents an error when no relevant data is found during a search. This class is a
    subclass of EphapticOSValidationError.

    Public methods:

    - __init__

    Instance variables:

    - message
    - name
    - status_code
    """

    def __init__(
        self,
        message: str = "Search did not find any data.",
        name: str = "NoRelevantDataError",
        status_code=status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(message, name, status_code)
