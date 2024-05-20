import operator
from functools import reduce
from transparent_classroom import models
from typing import Dict, List, Generic, TypeVar, Union, Any


_M = TypeVar('_M', bound=models.Model)


class Serializer(Generic[_M]):
    """
    Abstract Base Class for Object Serialization

    Attributes:
        mapping (`Dict[str, Union[str, List]])`: The object parameter to interface parameter mapping.

    """

    def __init__(self, mapping: Dict[str, Union[str, List]]) -> None:
        """
        Serializer Constructor

        :param mapping: Dict[str, Union[str, List]], The object parameter to interface parameter mapping.
        :return: None

        """

        self.mapping = mapping

    def serialize(self, obj: _M) -> Dict:
        """
        Serializer method for serializing the provided object.

        :param obj: _M, The object to serialize.
        :return: Dict

        """

        def get_from_dict(data_dict, map_list):
            try:
                return reduce(operator.getitem, map_list, data_dict)
            except Exception:
                return None

        def set_in_dict(data_dict: Dict, map_list: List, v: Any) -> None:
            if (map_list is not None) and (len(map_list) > 0):
                tmp = get_from_dict(data_dict, map_list[:(len(map_list) - 1)])

                if tmp is None:
                    set_in_dict(data_dict, map_list[:(len(map_list) - 1)], {})

                get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = v

        serialized_data, data = {}, obj.to_json()

        for object_key, interface_key in self.mapping.items():
            value = data.get(object_key, None)

            if value is not None:
                if isinstance(interface_key, str):
                    serialized_data[interface_key] = value
                elif isinstance(interface_key, list):
                    set_in_dict(serialized_data, interface_key, value)

        return serialized_data

    def batch(self, objs: Union[_M, List[_M]]) -> List[Dict]:
        """
        Batch serialize the objects.

        :param objs: Union[_M, List[_M]], The object to serialize.
        :return: List[Dict]

        """

        serialized_objects = []
        objs = objs if isinstance(objs, list) else [objs]

        for obj in objs:
            serialized_objects.append(self.serialize(obj=obj))

        return serialized_objects

    @property
    def mapping(self) -> Dict[str, Union[str, List]]:
        """
        The object parameter to interface parameter mapping.

        :return: Dict[str, Union[str, List]]

        """

        return self._mapping

    @mapping.setter
    def mapping(self, value: Dict[str, Union[str, List]]) -> None:
        """
        Set the object parameter to interface parameter mapping.

        :param value: Dict[str, Union[str, List]], The object parameter to interface parameter mapping.
        :return: None

        """

        self._mapping = value


class ChildSerializer(Serializer[models.Child]):
    """
    Child Serializer Class

    This class will serialize the Child object into a JSON-like string/dict that
    matches the parameter definition of the API interface.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Child Serializer Constructor

        :return: None

        """

        super().__init__(
            mapping={
                "first_name": "first_name",
                "last_name": "last_name",
                "birth_date": "birth_date",
                "gender": "gender",
                "program": "program",
                "ethnicity": "ethnicity",
                "household_income": "household_income",
                "dominant_language": "dominant_language",
                "grade": "grade",
                "student_id": "student_id",
                "hours_string": "hours_string",
                "allergies": "allergies",
                "notes": "notes"
            }
        )


class OnlineApplicationSerializer(Serializer[models.OnlineApplication]):
    """
    Online Application Serializer Class

    This class will serialize the Online Application object into a JSON-like string/dict that
    matches the parameter definition of the API interface.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Online Application Serializer Constructor

        :return: None

        """

        super().__init__(
            mapping={
                "id": "id",
                "school_id": "school_id",
                "type": "type",
                "state": "state",
                "fields": "fields"
            }
        )
