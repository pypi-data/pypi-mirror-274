from typing import Any


class InterfaceValidationError(ValueError):
    def __init__(self, field: str, value: Any, message: str) -> None:
        """

        :param field: str, The name of the interface field that raised the error.
        :param value: Any, The binding value that is invalid.
        :param message: str, The error message that was received and caught
            while doing field validation.
        :return: None

        """

        error_message = f"\n-> Invalid Field Assignment: {field}={value} ({message})."
        super().__init__(error_message)
