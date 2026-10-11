from fastapi import status

from EphapticOS.exceptions import (
    EphapticOSConfigurationError,
    EphapticOSValidationError,
)


class InvalidDataChunksError(EphapticOSValidationError):
    def __init__(self, detail: str):
        super().__init__(
            message=f"Invalid data_chunks: {detail}",
            name="InvalidDataChunksError",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class InvalidGraphModelError(EphapticOSValidationError):
    def __init__(self, got):
        super().__init__(
            message=f"graph_model must be a subclass of BaseModel (got {got}).",
            name="InvalidGraphModelError",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class InvalidOntologyAdapterError(EphapticOSConfigurationError):
    def __init__(self, got):
        super().__init__(
            message=f"ontology_adapter lacks required interface (got {got}).",
            name="InvalidOntologyAdapterError",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class InvalidChunkGraphInputError(EphapticOSValidationError):
    def __init__(self, detail: str):
        super().__init__(
            message=f"Invalid chunk inputs or LLM Chunkgraphs: {detail}",
            name="InvalidChunkGraphInputError",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class InvalidReferenceTypeError(EphapticOSValidationError):
    def __init__(self, detail: str):
        super().__init__(
            message=detail,
            name="InvalidReferenceTypeError",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
