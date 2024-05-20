import abc
import numbers
from datetime import date, datetime
from typing import Any, Union, Optional, Type, List
from transparent_classroom.api.interfaces.validators import exceptions


class Constraint(abc.ABC):
    """
    Constraint Class

    Constraints can be added to validators to check value assignments.

    Attributes:
        nullable (`bool`): Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.

    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.

        """

        self.nullable = nullable

    @abc.abstractmethod
    def __copy__(self) -> 'Constraint':
        """
        Copy and return the constraint object.

        :return: Constraint

        :raises: NotImplementedError

        """

        raise NotImplementedError()

    def __eq__(self, other: 'Constraint') -> bool:
        """
        Evaluate whether the two constraints are equal.

        :param other: Constraint, The other constraint to compare this
            constraint against.
        :return: bool

        """

        if other is None:
            return False

        return isinstance(other, Constraint) \
            and (self.__hash__() == other.__hash__()) \
            and (self.nullable == other.nullable)

    def __hash__(self) -> int:
        """
        Hash the constraint.

        :return: int

        """

        return hash(f"{self.__class__.__name__}<nullable={self.nullable}>")

    @abc.abstractmethod
    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Check whether the provided meets the constraint condition.

        :param value: Any, The value to match against the constraint.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        :raises: NotImplementedError

        """

        raise NotImplementedError()

    def is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Check whether the provided meets the constraint condition.

        :param value: Any, The value to match against the constraint.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        :raises: NullFieldException

        """

        if value is not None:
            return self._is_valid(value=value, strict=strict)
        elif self.nullable:
            return True
        elif strict:
            raise exceptions.NullFieldException()
        else:
            return False

    @property
    def nullable(self) -> bool:
        """
        Get the nullable flag.

        :return: bool

        """

        return self._nullable

    @nullable.setter
    def nullable(self, value: bool) -> None:
        """
        Set the nullable flag.

        :param value: bool, The boolean value indicating whether
            the constraint should operate on null values.
        :return: None

        """

        self._nullable = value


class IsType(Constraint):
    """
    Is Type Constraint Class

    Constraint class for validating whether a binding value is a specific type.

    Attributes:
        data_type (`Type`): The type to constrain the value to.
        exception_type (`Type`): The type of exception to raise if the constraint fails.

    """

    def __init__(self, data_type: Type, exception_type: Type, nullable: Optional[bool] = True) -> None:
        """
        Is Type Constraint Constructor

        :param data_type: Type, The type to constrain the value to.
        :param exception_type: Type, The type of exception to raise if the constraint fails.
        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.

        """

        super().__init__(nullable=nullable)
        self.data_type = data_type
        self.exception_type = exception_type

    def __copy__(self) -> 'IsType':
        """
        Copy the IsType Constraint

        :return: IsType

        """

        return IsType(data_type=self.data_type, exception_type=self.exception_type, nullable=self.nullable)

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is the constrained type.

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        is_valid = isinstance(value, self.data_type)

        if strict and (not is_valid):
            raise self.exception_type(value=value)

        return is_valid

    @property
    def data_type(self) -> Type:
        """
        Get the type to constrain the value to.

        :return: Type

        """

        return self._data_type

    @data_type.setter
    def data_type(self, value: Type) -> None:
        """
        Set the type to constrain the value to.

        :param value: Type, The type to constrain the value to.
        :return: None

        """

        self._data_type = value

    @property
    def exception_type(self) -> Type:
        """
        Get the type of exception to raise if the constraint fails.

        :return: Type

        """

        return self._exception_type

    @exception_type.setter
    def exception_type(self, value: Type) -> None:
        """
        Set the type of exception to raise if the constraint fails.

        :param value: Type, The type of exception to raise if the
            constraint fails.
        :return: None

        """

        self._exception_type = value


class IsNumeric(IsType):
    """
    Is Numeric Constraint Class

    Constraint class for validating whether a value is numeric.

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is Numeric Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.
        :return: None

        """

        IsType.__init__(
            self,
            data_type=numbers.Number,
            exception_type=exceptions.NumericValueError,
            nullable=nullable
        )

    def __copy__(self) -> 'IsNumeric':
        """
        Copy the Is Numeric Constraint

        :return: IsNumeric

        """

        return IsNumeric(nullable=self.nullable)

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is the constrained type.

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        is_valid = super()._is_valid(value=value, strict=strict)

        if is_valid and (value is not None):
            if isinstance(value, bool):
                if strict:
                    raise exceptions.NumericValueError(value=value)
                else:
                    is_valid = False

        return is_valid


class IsInteger(IsNumeric):
    """
    Is Integer Constraint Class

    Constraint class for validating whether a value is an integer.

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is Integer Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.
        :return: None

        """

        super().__init__(nullable=nullable)
        self.data_type = int
        self.exception_type = exceptions.IntegerValueError

    def __copy__(self) -> 'IsInteger':
        """
        Copy the Is Integer Constraint

        :return: IsInteger

        """

        return IsInteger(nullable=self.nullable)

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is the constrained type.

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        try:
            return super()._is_valid(value=value, strict=strict)
        except exceptions.NumericValueError:
            raise exceptions.IntegerValueError(value=value)


class IsGreaterThan(IsNumeric):
    """
    Is Greater Than Constraint

    Constraint for identifying if a value is numeric and
    greater than a specified value.

    Attributes:
        min_value (`Union[int, float]`): The minimum value to compare
            to. Constraint will check if the provided value > min_value.

    """

    def __init__(self, min_value: Optional[Union[int, float]] = 0, nullable: Optional[bool] = True) -> None:
        """
        Is Greater Than Constraint Constructor

        :param min_value: Union[int, float], The minimum value to compare
            to. Constraint will check if the provided value > min_value.
        :param nullable:Optional[Union[int, float]], Flag indicating whether null/None values
            are allowed. In which case, validation will only occur if a non-NoneType value
            is provided to the constraint.

        """

        self.min_value = min_value
        super().__init__(nullable=nullable)

    def __copy__(self) -> 'IsGreaterThan':
        """
        Copy the Is Greater Than Constraint

        :return: IsGreaterThan

        """

        return IsGreaterThan(min_value=self.min_value, nullable=self.nullable)

    def __hash__(self) -> int:
        """
        Hash the constraint.

        :return: int

        """

        return hash(" ".join([self.__class__.__name__, f"'value > {self.min_value}'", f"nullable={self.nullable}"]))

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is greater than the provided value.

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        is_valid = super()._is_valid(value=value, strict=strict)

        if is_valid:
            is_valid = is_valid and (value > self.min_value)

            if strict and (not is_valid):
                raise exceptions.NotGreaterThanValueError(value=value, min_value=self.min_value)

        return is_valid

    @property
    def min_value(self) -> Union[int, float]:
        """
        Get the min value of the constraint.

        :return: Union[int, float]

        """

        return self._method

    @min_value.setter
    def min_value(self, value: Union[int, float]) -> None:
        """
        Set the min value of the constraint.

        :param value: Union[int, float], The min value to set.
        :return: None

        """

        self._method = value


class IsPositiveInteger(IsGreaterThan, IsInteger):
    """
    Is Positive Integer Constraint Class

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is Positive Integer Constraint Constructor

        :param nullable: bool, Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
        :return: None

        """

        IsGreaterThan.__init__(self, min_value=0, nullable=nullable)
        IsInteger.__init__(self, nullable=nullable)

    def __copy__(self) -> 'IsPositiveInteger':
        """
        Copy the Is Positive Integer Constraint

        :return: IsPositiveInteger

        """

        return IsPositiveInteger(nullable=self.nullable)

    def __hash__(self) -> int:
        """
        Hash the constraint.

        :return: int

        """

        return Constraint.__hash__(self)

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is a positive integer.

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        is_valid = IsInteger._is_valid(self, value=value, strict=strict)
        return is_valid and IsGreaterThan._is_valid(self, value=value, strict=strict)


class IsBoolean(Constraint):
    """
    Is Boolean Constraint Class

    Constraint class for validating whether a value is boolean.

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is Boolean Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.
        :return: None

        """

        super().__init__(nullable=nullable)

    def __copy__(self) -> 'IsBoolean':
        """
        Copy the Is Boolean Constraint

        :return: IsBoolean

        """

        return IsBoolean(nullable=self.nullable)

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is a boolean string ("true", "false")

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        is_valid = True

        if value is not None:
            is_valid = isinstance(value, str) and ((value == "true") or (value == "false"))

        return is_valid


class IsRequired(Constraint):
    """
    Is Required Constraint Class

    Constraint class for validating a required field.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Is Required Constraint Constructor

        :return: None

        """

        super().__init__(nullable=False)

    def __copy__(self) -> 'IsRequired':
        """
        Copy the Is Required Constraint

        :return: IsRequired

        """

        return IsRequired()

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is required.

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        return value is not None


class IsString(IsType):
    """
    Is String Constraint Class

    Constraint class for validating a string value binding to a field.

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is Boolean Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.
        :return: None

        """

        super().__init__(
            data_type=str,
            exception_type=exceptions.StringValueError,
            nullable=nullable
        )

    def __copy__(self) -> 'IsString':
        """
        Copy the Is String Constraint

        :return: IsString

        """

        return IsString(nullable=self.nullable)


class IsDate(IsType):
    """
    Is Date Constraint Class

    Constraint class for validating a date value binding to a field.

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is Date Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.
        :return: None

        """

        super().__init__(
            data_type=date,
            exception_type=exceptions.DateValueError,
            nullable=nullable
        )

    def __copy__(self) -> 'IsDate':
        """
        Copy the Is Date Constraint

        :return: IsDate

        """

        return IsDate(nullable=self.nullable)

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Return whether the provided value is the constrained type.

        :param value: Any, The value to check the validity of.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        is_valid = super()._is_valid(value=value, strict=strict)

        if is_valid and (value is not None):
            if isinstance(value, datetime):
                if strict:
                    raise exceptions.DateValueError(value=value)
                else:
                    is_valid = False

        return is_valid


class IsDateTime(IsType):
    """
    Is DateTime Constraint Class

    Constraint class for validating a datetime value binding to a field.

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is DateTime Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.
        :return: None

        """

        super().__init__(
            data_type=datetime,
            exception_type=exceptions.DateTimeValueError,
            nullable=nullable
        )

    def __copy__(self) -> 'IsDateTime':
        """
        Copy the Is DateTime Constraint

        :return: IsDateTime

        """

        return IsDateTime(nullable=self.nullable)


class SelectionConstraint(Constraint):
    """
    Selection Constraint

    Constraint used to limit input values to a curated list of valid items.

    Attributes:
        options (`List`): A list of options that the provided value can be
            drawn from. Other values will be invalid.

    """

    def __init__(self, options: List, nullable: Optional[bool] = True) -> None:
        """
        Constraint Constructor

        :param options: List, A list of options that the provided value can be
            drawn from. Other values will be invalid.
        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.

        """

        super().__init__(nullable=nullable)
        self.options = options

    def __copy__(self) -> 'SelectionConstraint':
        """
        Copy the Selection Constraint

        :return: SelectionConstraint

        """

        return SelectionConstraint(options=self.options, nullable=self.nullable)

    def __eq__(self, other: 'Constraint') -> bool:
        """
        Evaluate whether the two constraints are equal.

        :param other: Constraint, The other constraint to compare this
            constraint against.
        :return: bool

        """

        is_valid = False

        if (other is not None) and isinstance(other, SelectionConstraint):
            is_valid = (set(self.options) == set(other.options)) and (self.nullable == other.nullable)

        return is_valid

    def __hash__(self) -> int:
        """
        Hash the constraint.

        :return: int

        """

        items = sorted(list(set(self.options)))
        return hash(f"{self.__class__.__name__}<nullable={self.nullable}> - ({items})")

    def _is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Check whether the provided meets the constraint condition.

        :param value: Any, The value to match against the constraint.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        """

        value_list = value if isinstance(value, list) else [value]

        for item in value_list:
            is_valid = item in self.options

            if is_valid:
                item_indices = [i for i in range(len(self.options)) if self.options[i] == item]
                is_valid = False

                for item_index in item_indices:
                    if (isinstance(item, type(self.options[item_index])) and
                            isinstance(self.options[item_index], type(item))):
                        is_valid = True
                        break

            if not is_valid:
                if strict:
                    raise exceptions.SelectionValueError(value=item, options=self.options)
                else:
                    return is_valid

        return True

    def is_valid(self, value: Any, strict: Optional[bool] = False) -> bool:
        """
        Check whether the provided meets the constraint condition.

        :param value: Any, The value to match against the constraint.
        :param strict: Optional[bool], Flag indicating whether to strictly enforce the
            constraint and raise an exception if the constraint fails.
        :return: bool

        :raises: NullFieldException

        """

        value = None if isinstance(value, list) and (len(value) == 0) else value
        return super().is_valid(value=value, strict=strict)

    @property
    def options(self) -> List:
        """
        Get the valid options for the constraint.

        :return: List

        """

        return self._options

    @options.setter
    def options(self, value: List) -> None:
        """
        Set the valid options for the constraint.

        :param value: List, The valid options for the constraint.
        :return: None

        """

        self._options = value


class IsList(IsType):
    """
    Is List Constraint Class

    Constraint class for validating a list value binding to a field.

    Attributes:


    """

    def __init__(self, nullable: Optional[bool] = True) -> None:
        """
        Is List Constraint Constructor

        :param nullable: Optional[bool], Flag indicating whether null/None values are
            allowed. In which case, validation will only occur if a non-NoneType
            value is provided to the constraint.
        :return: None

        """

        super().__init__(
            data_type=list,
            exception_type=exceptions.ListValueError,
            nullable=nullable
        )

    def __copy__(self) -> 'IsList':
        """
        Copy the Is List Constraint

        :return: IsList

        """

        return IsList(nullable=self.nullable)
