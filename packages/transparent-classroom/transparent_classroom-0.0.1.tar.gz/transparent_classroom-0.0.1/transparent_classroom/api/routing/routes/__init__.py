from typing import List, Union, Dict
from transparent_classroom.api.enums import ModelType


class RouteComponent(object):
    """
    Route Component Class

    Attributes:
        sub_path (`str`): A sub-path in the API route.

    """

    def __init__(self, sub_path: str) -> None:
        """
        Route Component constructor

        :param sub_path: str, A sub-path in the API route.
        :return: None

        """

        self.sub_path = sub_path

    def __copy__(self) -> 'RouteComponent':
        """
        Copy the Route Component

        :return: RouteComponent

        """

        return RouteComponent(sub_path=self.sub_path)

    def __eq__(self, other: 'RouteComponent') -> bool:
        """
        Compare whether the two components are equivalent.

        :param other: RouteComponent, The component to compare to.
        :return: bool

        """

        if (other is not None) and isinstance(other, RouteComponent):
            return self.sub_path == other.sub_path

        return False

    @property
    def sub_path(self) -> str:
        """
        Sub-path getter method.

        :return: str

        """

        return self._sub_path

    @sub_path.setter
    def sub_path(self, value: str) -> None:
        """
        Sub-path setter method.

        :param value: str, A sub-path in the API route.
        :return: None

        """

        if value is None:
            raise ValueError("Route components cannot be `None`.")

        self._sub_path = value.strip("/").strip("\\")


class Route(object):
    """
    Route Class

    Denotes an individual route to the API.

    Attributes:
        model_type (`ModelType`): The Transparent Classroom model/object being
            queried for on the API.
        suffix (`str`): The suffix (if any) to append to the end of the path.

    """

    def __init__(self, model_type: ModelType, components: List[RouteComponent], suffix: str = ".json") -> None:
        """
        Route Object Constructor

        :param model_type: ModelType, The Transparent Classroom model/object being
            queried for on the API.
        :param components:  List[RouteComponent], Route components defining the
            overall route path.
        :param suffix: str, A suffix value to add onto the route.
        :return: None

        """

        self.model_type = model_type
        self._components = []
        self.suffix = suffix
        self.add(components=components)

    def __eq__(self, other: 'Route') -> bool:
        """
        Evaluate whether the two routes have the same path.

        :param other: Route, The route to compare to.
        :return: bool

        """

        if (other is not None) and isinstance(other, Route):
            return (self.path == other.path) and (self.model_type == other.model_type)

        return False

    def apply(self, **kwargs: Dict) -> str:
        """
        Apply the specified variables to the route, if it contains components that
        should be filled with variable values.

        :param kwargs: Dict, The variable assignments to apply to the route.
        :return: str

        """

        path = self.path

        for k in kwargs.keys():
            variable = "{{ " + k + " }}"
            path = path.replace(variable, str(kwargs[k]))

        return path

    def add(self, components: Union[RouteComponent, List[RouteComponent]]) -> None:
        """

        :param components: Union[RouteComponent, List[RouteComponent]], The
            component(s) to add to the route.
        :return: None

        """

        components = [components] if isinstance(components, RouteComponent) else components

        for component in components:
            if isinstance(component, RouteComponent):
                self._components.append(component)

    def remove(self, components: Union[RouteComponent, List[RouteComponent]]) -> None:
        """

        :param components: Union[RouteComponent, List[RouteComponent]], The
            component(s) to remove from the route.
        :return: None

        """

        components = [components] if isinstance(components, RouteComponent) else components

        for component in components:
            if isinstance(component, RouteComponent):
                if component in self._components:
                    self._components.remove(component)

    @property
    def path(self) -> str:
        """
        Get the path of the route.

        :return: str

        """

        path = "/".join([component.sub_path for component in self.components])
        return path + self.suffix if self.suffix is not None else path

    @property
    def model_type(self) -> ModelType:
        """
        The Transparent Classroom model/object being queried for on the API.

        :return: ModelType

        """

        return self._model_type

    @model_type.setter
    def model_type(self, value: ModelType) -> None:
        """
        Model setter method.

        :param value: ModelType, The Transparent Classroom model/object being
            queried for on the API.
        :return: None

        """

        self._model_type = value

    @property
    def components(self) -> List[RouteComponent]:
        """
        The list of components comprising the route path.

        :return: List[RouteComponent]

        """

        return [component.__copy__() for component in self._components]

    @property
    def suffix(self) -> str:
        """
        The Transparent Classroom model/object being queried for on the API.

        :return: str

        """

        return self._suffix

    @suffix.setter
    def suffix(self, value: str) -> None:
        """
        Setter for the route/path suffix.

        :param value: str, The suffix to append to the path.
        :return: None

        """

        self._suffix = value
