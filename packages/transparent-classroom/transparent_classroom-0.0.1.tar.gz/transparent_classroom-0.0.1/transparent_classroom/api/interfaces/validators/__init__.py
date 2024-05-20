from typing import Union, Optional, List, Any
from transparent_classroom.api.interfaces.validators.constraints import Constraint, IsRequired


class Validator(object):
    """
    Validator Class

    Constraint container class that allows for constraints to be applied
    against a given value.

    Attributes:


    """

    def __init__(
            self,
            constraints: Optional[Union[Constraint, List[Constraint]]] = None,
            is_required: Optional[bool] = False) -> None:
        """
        Validator Constructor

        :param constraints: Optional[Union[Constraint, List[Constraint]]], The constraints
            to enforce using this constraint.
        :param is_required: Optional[bool], Flag indicating whether the constraints are non-nullable
            or nullable.
        :return: None

        """

        self._is_required = is_required
        self._constraints = []
        self.add(constraints=constraints)

    def __eq__(self, other: Any) -> bool:
        """
        Check whether the other validator is equal to this validator.

        :param other: Any, The other validator that is being checked for equality.
        :return: bool

        """

        if (other is not None) and isinstance(other, Validator) and (len(self) == len(other)):
            is_equal = True

            for constraint in self._constraints:
                if constraint not in other:
                    is_equal = False
                    break

            return is_equal

        return False

    def __contains__(self, item: Any) -> bool:
        """
        Tell if a constraint is inside the validator.

        :param item: Any, The item to check for containment.
        :return: bool

        """

        if (item is not None) and isinstance(item, Constraint):
            return item in self._constraints

        return False

    def __len__(self) -> int:
        """
        The number of constraints in the validator.

        :return: int

        """

        return len(self._constraints)

    def __copy__(self) -> 'Validator':
        """
        Copy the Validator

        :return: Validator

        """

        constraints = []

        for constraint in self._constraints:
            constraints.append(constraint.__copy__())

        return Validator(constraints=constraints, is_required=self.is_required)

    def add(self, constraints: Union[Constraint, List[Constraint]]) -> None:
        """
        Add the specified constraint(s) to the validator.

        :param constraints: Union[Constraint, List[Constraint]], The constraints
            to add to the validator.
        :return: None

        """

        if constraints is not None:
            change_to_required = False
            constraints = constraints if isinstance(constraints, list) else [constraints]

            for constraint in constraints:
                if isinstance(constraint, Constraint) and (constraint not in self._constraints):
                    self._constraints.append(constraint)

                    if isinstance(constraint, IsRequired) and (not self.is_required):
                        change_to_required = True

            if change_to_required:
                self.is_required = True

    def clear(self) -> None:
        """
        Clear the constraints from the validator.

        :return: None

        """

        self._constraints = []
        self._is_required = False

    def remove(self, constraints: Union[Constraint, List[Constraint]]) -> None:
        """
        Remove the specified constraint(s) from the validator.

        :param constraints: Union[Constraint, List[Constraint]], The constraints
            to remove from the validator.
        :return: None

        """

        if constraints is not None:
            change_to_optional = False
            constraints = constraints if isinstance(constraints, list) else [constraints]

            for constraint in constraints:
                if isinstance(constraint, Constraint) and (constraint in self._constraints):
                    self._constraints.remove(constraint)

                    if isinstance(constraint, IsRequired) and self.is_required:
                        change_to_optional = True

            if change_to_optional:
                self.is_required = False

    def is_valid(self, value: Any, strict: bool = False) -> bool:
        """
        Determine whether the provided value matches all constraints.

        :param value: Any, The value to check against the constraints.
        :param strict: bool, Flag indicating whether to strictly enforce the
            validator constraints and raise an exception if an error occurs.
        :return: bool

        """

        for constraint in self._constraints:
            if not constraint.is_valid(value=value, strict=strict):
                return False

        return True

    @property
    def is_required(self) -> bool:
        """
        Set the flag for requiring non-nullable validation.

        :return: bool

        """

        return self._is_required

    @is_required.setter
    def is_required(self, value: bool) -> None:
        """
        Set whether the validator is required.

        :param value: bool, Flag indicating whether the field is required.
        :return: None

        """

        self._is_required = value

        for i in range(0, len(self._constraints)):
            self._constraints[i].nullable = not self._is_required

        if self._is_required and (IsRequired() not in self._constraints):
            self.add(constraints=IsRequired())
        elif (not self._is_required) and (IsRequired() not in self._constraints):
            self.remove(constraints=IsRequired())
