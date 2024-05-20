from datetime import date, datetime
from typing import List, Any, Union, Generic, TypeVar, Dict, Optional
from transparent_classroom.api.interfaces.validators import constraints, Validator
from transparent_classroom.api.interfaces.validators.exceptions import ConstraintException
from transparent_classroom.api.interfaces.fields.exceptions import InterfaceValidationError


class NamedAPIAttribute(object):
    """
    Named API Attribute Class

    Class for named API attributes.

    Attributes:
        name (`str`): The name of the api attribute.

    """

    def __init__(self, name: str) -> None:
        """
        Construct the Named API Attribute.

        :param name: str, The name of the attribute.

        """

        self._name = name

    def __eq__(self, other: Any) -> bool:
        """
        Evaluate whether the other object and this attribute are the same.

        :param other: Attribute, The attribute to compare to.
        :return: bool

        """

        if (other is None) or (not isinstance(other, NamedAPIAttribute)):
            return False

        return (other.name == self.name) and (str(self) == str(other))

    def __str__(self) -> str:
        """
        The string representation of the name API attribute.

        :return: str

        """

        return f"Attribute `{self.name}`"

    def __repr__(self) -> str:
        """
        The string representation of the named API attribute.

        :return: str

        """

        return str(self)

    def __hash__(self) -> int:
        """
        Hash the attribute.

        :return: int

        """

        return hash(str(self))

    @property
    def name(self) -> str:
        """
        Get the name of the API attribute.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the API attribute.

        :param value: str, The name of the API attribute to set.
        :return: None

        """

        self._name = value


class Field(NamedAPIAttribute):
    """
    Field Class

    Attributes:
        name (`str`): The name of the api attribute.
        value (`Any`): The value bound to this variable.
        is_required (`bool`): Flag indicating whether the field is required.
        validator (`Validator`): The validator to use when validating
            the field binding.

    """

    def __init__(
            self,
            name: str,
            value: Optional[Any] = None,
            is_required: Optional[bool] = False,
            validator: Optional[Validator] = None) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param value: Optional[Any], The value bound to this variable.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :param validator: Optional[Validator], The validator to use when validating the
            field binding.

        """

        super().__init__(name=name)
        self.value = value
        self.validator = validator
        self.is_required = is_required

    def __copy__(self) -> 'Field':
        """
        Copy the field object.

        :return: Field

        """

        return Field(
            name=self.name,
            value=self.value,
            validator=self.validator.__copy__(),
            is_required=self.is_required
        )

    def __eq__(self, other: 'Field') -> bool:
        """
        Evaluate whether the other field (and binding) are the same.

        :param other: Field, The field compare to.
        :return: bool

        """

        if (other is None) or (not isinstance(other, Field)):
            return False

        return (other.name == self.name) \
            and (other.value == self.value) \
            and (self.validator == other.validator)

    def __str__(self) -> str:
        """
        The string representation of the field.

        :return: str

        """

        return f"Field `{self.name}` = {self.value}"

    def __repr__(self) -> str:
        """
        The string representation of the field.

        :return: str

        """

        return str(self)

    def __hash__(self) -> int:
        """
        Hash the field.

        :return: int

        """

        return hash(str(self))

    def is_valid(self, strict: bool = False) -> bool:
        """
        Return whether the field assignment is valid.

        :param strict: bool, Flag indicating whether to perform strict validation.
        :return: bool

        """

        return self.validator.is_valid(value=self.value, strict=strict)

    @property
    def name(self) -> str:
        """
        Get the name of the variable.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the field.

        :param value: str, The name of the field to set.
        :return: None

        """

        self._name = value

    @property
    def value(self) -> Any:
        """
        Get the value bound to the field.

        :return: Any

        """

        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """
        Set the value to bind to the field.

        :param value: Any, The value to bind to the field.
        :return: None

        """

        self._value = value

    @property
    def validator(self) -> Validator:
        """
        Get the validator of the field.

        :return: Validator

        """

        return self._validator

    @validator.setter
    def validator(self, value: Validator) -> None:
        """
        Set the field validator.

        :param value: Validator, The validator to use when validating
            the contents of a field.
        :return: None

        """

        self._validator = Validator() if value is None else value

    @property
    def is_required(self) -> bool:
        """
        Get the flag for requiring a value in this field.

        :return: bool

        """

        return self._validator.is_required

    @is_required.setter
    def is_required(self, value: bool) -> None:
        """
        Set whether the field is required.

        :param value: bool, Flag indicating whether the field is required.
        :return: None

        """

        self._validator.is_required = value


class PositiveIntegerField(Field):
    """
    Positive Integer Field Class

    Attributes:


    """

    def __init__(self, name: str, value: Optional[int] = None, is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param value: Optional[int], The value bound to this variable.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        super().__init__(
            name=name,
            value=value,
            is_required=is_required,
            validator=Validator(
                constraints=[
                    constraints.IsPositiveInteger()
                ]
            )
        )


class ModelIdField(PositiveIntegerField):
    """
    Model Identification Field Class

    Attributes:


    """

    def __init__(self, name: str, value: Optional[int] = None, is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param value: Optional[int], The value bound to this variable.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        super().__init__(
            name=name,
            value=value,
            is_required=is_required
        )


class StringField(Field):
    """
    String Field Class

    Attributes:


    """

    def __init__(self, name: str, value: Optional[str] = None, is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param value: Optional[str], The value bound to this variable.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        super().__init__(
            name=name,
            value=value,
            is_required=is_required,
            validator=Validator(
                constraints=[
                    constraints.IsString()
                ]
            )
        )


class BooleanField(Field):
    """
    Boolean Field Class

    Attributes:


    """

    def __init__(self, name: str, value: Optional[str] = None, is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param value: Optional[str], The value bound to this variable. Boolean parameters
            on the API are strings ("true", "false").
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        super().__init__(
            name=name,
            value=value,
            is_required=is_required,
            validator=Validator(
                constraints=[
                    constraints.IsBoolean()
                ]
            )
        )


class DateField(Field):
    """
    Date Field Class

    Attributes:
        format (`str`): The format the date value should be formatted to.

    """

    def __init__(
            self,
            name: str,
            value: Optional[date] = None,
            format: Optional[str] = "%Y-%m-%d",
            is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param value: Optional[date], The value bound to this variable.
        :param format: Optional[str], The format the date value should be formatted to.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        super().__init__(
            name=name,
            value=value,
            is_required=is_required,
            validator=Validator(
                constraints=[
                    constraints.IsDate()
                ]
            )
        )
        self.format = format

    @property
    def format(self) -> str:
        """
        Get the format the date value should be formatted to.

        :return: str

        """

        return self._format

    @format.setter
    def format(self, value: str) -> None:
        """
        Set the format the date value should be formatted to.

        :param value: str, The string format of the date.
        :return: None

        """

        self._format = value


class DateTimeField(Field):
    """
    Date Time Field Class

    Attributes:
        format (`str`): The format the datetime value should be formatted to.

    """

    def __init__(
            self,
            name: str,
            value: Optional[datetime] = None,
            format: Optional[str] ="%Y-%m-%dT%H:%M:%S.%f%z",
            is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param value: Optional[datetime], The value bound to this variable.
        :param format: Optional[str], The format the date value should be formatted to.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        super().__init__(
            name=name,
            value=value,
            is_required=is_required,
            validator=Validator(
                constraints=[
                    constraints.IsDateTime()
                ]
            )
        )
        self.format = format

    @property
    def format(self) -> str:
        """
        Get the format the datetime value should be formatted to.

        :return: str

        """

        return self._format

    @format.setter
    def format(self, value: str) -> None:
        """
        Set the format the datetime value should be formatted to.

        :param value: str, The string format of the datetime.
        :return: None

        """

        self._format = value


class SelectField(Field):
    """
    Select Field Class

    Attributes:


    """

    def __init__(
            self,
            name: str,
            options: List,
            value: Optional[Any] = None,
            is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param options: List, A list of options that the provided value can be
            drawn from. Other values will be invalid.
        :param value: Optional[Any], The value bound to this variable.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        self._options_constraint = constraints.SelectionConstraint(options=options)
        super().__init__(
            name=name,
            value=value,
            is_required=is_required,
            validator=Validator(
                constraints=[
                    self._options_constraint
                ]
            )
        )

    @property
    def options(self) -> List:
        """
        Get the valid options for the field.

        :return: List

        """

        return self._options_constraint.options

    @options.setter
    def options(self, value: List) -> None:
        """
        Set the valid options for the field.

        :param value: List, The valid options for the field.
        :return: None

        """

        self._options_constraint.options = value


class MultiSelectField(Field):
    """
    MultiSelect Field Class

    Attributes:


    """

    def __init__(
            self,
            name: str,
            options: List,
            value: Optional[List] = None,
            is_required: Optional[bool] = False) -> None:
        """
        Construct the fields and it's assignment.

        :param name: str, The name of the variable.
        :param options: List, A list of options that the provided value can be
            drawn from. Other values will be invalid.
        :param value: Optional[List], The value bound to this variable.
        :param is_required: Optional[bool], Flag indicating whether the field is required.
        :return: None

        """

        self._options_constraint = constraints.SelectionConstraint(options=options)
        super().__init__(
            name=name,
            value=value,
            is_required=is_required,
            validator=Validator(
                constraints=[
                    self._options_constraint,
                    constraints.IsList()
                ]
            )
        )

    @property
    def options(self) -> List:
        """
        Get the valid options for the field.

        :return: List

        """

        return self._options_constraint.options

    @options.setter
    def options(self, value: List) -> None:
        """
        Set the valid options for the field.

        :param value: List, The valid options for the field.
        :return: None

        """

        self._options_constraint.options = value


class InterfaceField(NamedAPIAttribute):
    """
    Interface Field Class

    Class for managing interface fields

    Attributes:
        base (`Field`): The base field that interface is wrapping and performing
            validation for (on the entrypoint interface).

    """

    def __init__(self, base: Field) -> None:
        """
        Construct the interface field.

        :param base: str, The name of the variable.

        """

        self.base = base
        super().__init__(name=self.name)

    def __str__(self) -> str:
        """
        The string representation of the variable.

        :return: str

        """

        return f"Interface Field `{self.name}`"

    def __repr__(self) -> str:
        """
        The string representation of the variable.

        :return: str

        """

        return str(self)

    def __copy__(self) -> 'InterfaceField':
        """
        Copy the interface field object.

        :return: InterfaceField

        """

        return InterfaceField(
            base=self.base.__copy__()
        )

    def is_valid(self, value: Any, strict: bool = False) -> bool:
        """
        Return whether the value assignment is valid.

        :param value: Any, The value to check for validity.
        :param strict: bool, Flag indicating whether to strictly enforce the
            validator constraints and raise an exception if an error occurs.
        :return: bool

        """

        return self.base.validator.is_valid(value=value, strict=strict)

    def bind(self, value: Any) -> Field:
        """
        Bind the value and produce the associated field.

        :param value: Any, The value to bind.
        :return: Field

        """

        if self.is_valid(value=value, strict=True):
            field_type = type(self.base)
            name = self.name.replace("_interface_field", "")
            return field_type(name=name, value=value)

    @property
    def name(self) -> Any:
        """
        Get the name of the interface field.

        :return: Any

        """

        return f"{self.base.name}_interface_field"

    @name.setter
    def name(self, name: Any) -> None:
        """
        Set the name of the interface field.

        :param name: Any, The value of the interface field name.
        :return: None

        """

        raise NotImplementedError()


T = TypeVar('T', bound=Union[Field, NamedAPIAttribute])


class FieldSet(Generic[T]):
    """
    Field Set

    Container object for fields and their bindings.

    Attributes:


    """

    def __init__(self, fields: Optional[Union[T, List[T]]] = None) -> None:
        """
        Field Set Constructor

        :param fields: Optional[Union[T, List[T]]], The fields to add to the field set.
        :return: None

        """

        self._fields = {}
        self.add(fields=fields)

    def __len__(self) -> int:
        """
        Get the number of items in the field set.

        :return: int

        """

        return len(self._fields)

    def __getitem__(self, arg: str) -> Union[None, T]:
        """
        Get the field.

        :param arg: str, The name of the field to get.
        :return: Union[None, T]

        """

        return self.get(name=arg)

    def get(self, name: str) -> Union[None, T]:
        """
        Get the field.

        :param name: str, The name of the field to get.
        :return: Union[None, T]

        """

        if (name is not None) and (name in self._fields.keys()):
            return self._fields[name]

    def _add(self, field: T) -> None:
        """
        Add the field to the field set.

        :param field: T, A single field to add to the field set.
        :return: None

        """

        if field is not None:
            self._fields[field.name] = field

    def add(self, fields: Union[T, List[T], 'FieldSet']) -> None:
        """
        Add the fields to the field set.

        :param fields: Union[T, List[T], 'FieldSet'], The field(s_ to add to the
            field set.
        :return: None

        """

        if fields is not None:
            fields = fields.to_list() if isinstance(fields, FieldSet) else fields
            fields = fields if isinstance(fields, list) else [fields]

            for f in fields:
                if isinstance(f, NamedAPIAttribute):
                    self._add(field=f)

    def _remove(self, field: Union[T, str]) -> None:
        """
        Remove the field from the field set.

        :param field: Union[T, str], A field/name of a field to remove
            from the field set.
        :return: None

        """

        if field is not None:
            bk = field.name if not isinstance(field, str) else field

            if bk in self._fields.keys():
                del self._fields[bk]

    def remove(self, fields: Union[T, str, List[T], List[str], 'FieldSet']) -> None:
        """
        Remove the field(s) from the field set.

        :param fields: Union[T, str, List[T], List[str], 'FieldSet'], A list of
            fields, field names, or another field set to remove from the field set.
        :return: None

        """

        if fields is not None:
            fields = fields.to_list() if isinstance(fields, FieldSet) else fields
            fields = fields if isinstance(fields, list) else [fields]

            for f in fields:
                if isinstance(f, NamedAPIAttribute) or isinstance(f, str):
                    self._remove(field=f)

    def clear(self) -> None:
        """
        Clear the field set.

        :return: None

        """

        self._fields = {}

    def to_json(self) -> Dict:
        """
        Convert the field set into a JSON string/dict.

        :return: Dict

        """

        data = {}

        for field in self._fields.values():
            data[field.name] = field.value

        return data

    def to_list(self) -> List[T]:
        """
        Get the fields as a list.

        :return: List[T]

        """

        return [field.__copy__() for field in self._fields.values()]


class InterfaceFieldSet(FieldSet[InterfaceField]):
    """
    Interface Field Set

    Container object for interface fields.

    Attributes:


    """

    def __init__(self, fields: Optional[Union[InterfaceField, List[InterfaceField]]] = None) -> None:
        """
        Field Set Constructor

        :param fields: Optional[Union[InterfaceField, List[InterfaceField]]], The fields
            to add to the field set.
        :return: None

        """

        super().__init__(fields=fields)

    def add(self, fields: Union[InterfaceField, List[InterfaceField], 'InterfaceFieldSet']) -> None:
        """
        Add the fields to the field set.

        :param fields: Union[InterfaceField, List[InterfaceField], 'InterfaceFieldSet'],
            The field(s_ to add to the field set.
        :return: None

        """

        super().add(fields=fields)

    def remove(self, fields: Union[InterfaceField, str, List[InterfaceField], List[str], 'InterfaceFieldSet']) -> None:
        """
        Remove the field(s) from the field set.

        :param fields: Union[InterfaceField, str, List[InterfaceField], List[str], 'InterfaceFieldSet'],
            A list of fields, field names, or another field set to remove from the field set.
        :return: None

        """

        super().remove(fields=fields)

    def validate(self, bindings: Dict) -> Dict:
        """
        Validate all the configured bindings against the field set.

        :param bindings: Dict, The bindings to validate.
        :return: Dict

        """

        validated_bindings = {}

        for field in self._fields.values():
            key = field.base.name
            value = bindings[key] if key in bindings.keys() else None

            try:
                if field.base.validator.is_valid(value=value, strict=True) and (value is not None):
                    validated_bindings[key] = value
            except ConstraintException as e:
                raise InterfaceValidationError(field=key, value=value, message=str(e))

        return validated_bindings
