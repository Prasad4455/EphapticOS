from fastapi import status

from EphapticOS.exceptions import EphapticOSConfigurationError, EphapticOSSystemError, EphapticOSValidationError


class S3FileSystemNotFoundError(EphapticOSSystemError):
    def __init__(
        self,
        name: str = "S3FileSystemNotFoundError",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        message = "Could not find S3FileSystem."
        super().__init__(
            message,
            name,
            status_code,
            remediation=(
                'Install the aws extra (pip install "EphapticOS[aws]") so s3fs is available, and '
                "set AWS_REGION plus AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY (or a profile) "
                "when reading s3:// paths or using STORAGE_BACKEND=s3."
            ),
        )


class InvalidDLTArgumentError(EphapticOSValidationError):
    def __init__(
        self,
        name: str = "InvalidDLTArgumentError",
        message: str = "Invalid argument for dlt ingestion.",
        status_code: int = status.HTTP_422_UNPROCESSABLE_CONTENT,
    ):
        super().__init__(message, name, status_code)


class UnsupportedDBProviderError(EphapticOSConfigurationError):
    def __init__(
        self,
        name: str = "UnsupportedDBProviderError",
        message: str = "Unsupported database provider.",
        status_code: int = status.HTTP_422_UNPROCESSABLE_CONTENT,
    ):
        super().__init__(
            message,
            name,
            status_code,
            remediation=(
                "Set DB_PROVIDER to 'sqlite' (default) or 'postgres' (needs the postgres "
                'extra: pip install "EphapticOS[postgres]"); dlt ingestion writes to the same '
                "relational database EphapticOS uses."
            ),
        )


class DLTIngestionError(EphapticOSSystemError):
    def __init__(
        self,
        name: str = "DLTIngestionError",
        message: str = "Error in the execution of a DLT pipeline, and the extraction of its schema",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message, name, status_code)


class LabelCountMismatchError(EphapticOSValidationError):
    def __init__(
        self,
        message: str = "Label count does not match data item count.",
        name: str = "LabelCountMismatchError",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, name, status_code)


class InvalidLabelsError(EphapticOSValidationError):
    def __init__(
        self,
        message: str = 'labels must be a JSON array of strings, e.g. ["finance", ""].',
        name: str = "InvalidLabelsError",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, name, status_code)


class InvalidExternalMetadataError(EphapticOSValidationError):
    def __init__(
        self,
        message: str = (
            'external_metadata must be a JSON array of objects, e.g. [{"source": "crm"}, null].'
        ),
        name: str = "InvalidExternalMetadataError",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, name, status_code)


class ExternalMetadataCountMismatchError(EphapticOSValidationError):
    def __init__(
        self,
        message: str = "external_metadata count does not match data item count.",
        name: str = "ExternalMetadataCountMismatchError",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, name, status_code)
