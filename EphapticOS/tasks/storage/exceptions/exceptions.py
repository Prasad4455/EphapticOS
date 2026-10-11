from fastapi import status

from EphapticOS.exceptions import (
    EphapticOSValidationError,
)


class InvalidDataPointsInAddDataPointsError(EphapticOSValidationError):
    def __init__(self, detail: str):
        super().__init__(
            message=f"Invalid data_points: {detail}",
            name="InvalidDataPointsInAddDataPointsError",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
