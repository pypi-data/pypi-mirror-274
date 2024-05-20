import numbers
from datetime import date, datetime
from typing import Any, Union, Type, List


class ConstraintException(ValueError):
    """
    Generic Constraint Exception Class

    Attributes:


    """

    def __init__(self, message: str = None) -> None:
        """
        Constraint Exception Constructor

        :param message: str, The message to show when an exception has been encountered.
        :return: None

        """

        super().__init__(message)


class TypeConstraintException(ConstraintException):
    """
    Generic Type Constraint Exception Class

    Attributes:


    """

    def __init__(self, value: Any, data_type: Type) -> None:
        """
        Type Constraint Value Error Constructor

        :param value: Any, The value that failed validation.
        :param data_type: Type, The expected data type.
        :return: None

        """

        super().__init__(f"Field value `{value}` is not an instance of `{data_type}`")


class NullFieldException(ConstraintException):
    """
    Null Field Exception

    This exception should be thrown when a non-nullable field is validated and the
    input value is None.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Null Field Exception Constructor

        :return: None

        """

        super().__init__("Field value cannot be None")


class NumericValueError(TypeConstraintException):
    """
    Numeric Value Error Class

    This exception should be thrown when a non-numeric value is passed into a
    field with a numeric field constraint.

    Attributes:


    """

    def __init__(self, value: Any) -> None:
        """
        Numeric Constraint Value Error Constructor

        :param value: Any, The value that failed validation.
        :return: None

        """

        super().__init__(value=value, data_type=numbers.Number)


class IntegerValueError(TypeConstraintException):
    """
    Integer Value Error Class

    This exception should be thrown when a non-integer value is passed into a
    field with an integer field constraint.

    Attributes:


    """

    def __init__(self, value: Any) -> None:
        """
        Integer Constraint Value Error Constructor

        :param value: Any, The value that failed validation.
        :return: None

        """

        super().__init__(value=value, data_type=int)


class NotGreaterThanValueError(ConstraintException):
    """
    Not Greater Than Value Error Class

    This exception should be thrown when a value is provided that is not
    greater than the minimum threshold provided by a greater-than constraint.

    Attributes:


    """

    def __init__(self, value: Any, min_value: Union[int, float]) -> None:
        """
        Not Greater Than Value Error Constructor

        :param value: Any, The value that failed validation.
        :param min_value: Union[int, float], The floor value of the constraint.
        :return: None

        """

        super().__init__(f"Field value `{value}` is not greater than the minimum value `{min_value}`")


class StringValueError(TypeConstraintException):
    """
    String Value Error Class

    This exception should be thrown when a value is provided to a required
    field that is not a string (as expected).

    Attributes:


    """

    def __init__(self, value: Any) -> None:
        """
        Non-String Constraint Value Error Constructor

        :param value: Any, The value that failed validation.
        :return: None

        """

        super().__init__(value=value, data_type=str)


class DateValueError(TypeConstraintException):
    """
    Date Value Error Class

    This exception should be thrown when a value is provided to a required
    field that is not a date (as expected).

    Attributes:


    """

    def __init__(self, value: Any) -> None:
        """
        Date Constraint Value Error Constructor

        :param value: Any, The value that failed validation.
        :return: None

        """

        super().__init__(value=value, data_type=date)


class DateTimeValueError(TypeConstraintException):
    """
    Date Time Value Error Class

    This exception should be thrown when a value is provided to a required
    field that is not a datetime (as expected).

    Attributes:


    """

    def __init__(self, value: Any) -> None:
        """
        DateTime Constraint Value Error Constructor

        :param value: Any, The value that failed validation.
        :return: None

        """

        super().__init__(value=value, data_type=datetime)


class ListValueError(TypeConstraintException):
    """
    List Value Error Class

    This exception should be thrown when a value is provided to a required
    field that is not a list object (as expected).

    Attributes:


    """

    def __init__(self, value: Any) -> None:
        """
        List Constraint Value Error Constructor

        :param value: Any, The value that failed validation.
        :return: None

        """

        super().__init__(value=value, data_type=list)


class SelectionValueError(ConstraintException):
    """
    Selection Value Error Class

    This exception should be thrown when a value (or list of values) is provided that
    is/are not contained in the select options.

    Attributes:


    """

    def __init__(self, value: Any, options: List) -> None:
        """
        Not Greater Than Value Error Constructor

        :param value: Any, The value that failed validation.
        :param options: List, The list of valid options.
        :return: None

        """

        super().__init__(f"Field value `{value}` is not contained in `{options}`")