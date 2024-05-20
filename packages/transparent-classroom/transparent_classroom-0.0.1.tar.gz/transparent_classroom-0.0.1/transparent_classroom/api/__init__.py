from typing import List, Union, Optional
from transparent_classroom.api.entry_points import EntryPoint
from transparent_classroom.api.enums import EndpointBehavior, ModelType
from transparent_classroom.api.exceptions import EntrypointNotFoundException


class API(object):
    """
    API Class

    Collection of entry points defining the API.

    Attributes:


    """

    def __init__(self, entry_points: Optional[Union[EntryPoint, List[EntryPoint]]] = None) -> None:
        """
        API Class Constructor

        :param entry_points: Optional[Union[EntryPoint, List[EntryPoint]]], The entry
            point(s) to register with the API.
        :return: None

        """

        self._entry_points = {}
        self.register(entry_points=entry_points)

    def register(self, entry_points: Union[EntryPoint, List[EntryPoint]]) -> None:
        """
        Register the provided entry points with the API.

        :param entry_points: Optional[Union[EntryPoint, List[EntryPoint]]], The entry
            point(s) to register with the API.
        :return: None

        """

        if entry_points is not None:
            entry_points = [entry_points] if isinstance(entry_points, EntryPoint) else entry_points

            for entry_point in entry_points:
                model_type = entry_point.route.model_type.value
                behavior = entry_point.interface.behavior.value

                if model_type not in self._entry_points.keys():
                    self._entry_points[model_type] = {}

                if behavior in self._entry_points[model_type].keys():
                    path = entry_point.route.path
                    raise KeyError(f"A route has already been assigned to {model_type} -> {behavior}: {path}.")

                self._entry_points[model_type][behavior] = entry_point

    def clear(self) -> None:
        """
        Clear the API of its registered entry points.

        :return: None

        """

        self._entry_points = {}

    def unregister(self, entry_points: Union[EntryPoint, List[EntryPoint], str, List[str]]) -> None:
        """
        Unregister the provided entry points from the API.

        :param entry_points: Union[EntryPoint, List[EntryPoint], str, List[str]],
            The entry point(s) or names to remove from the API.
        :return: None

        """

        if entry_points is not None:
            entry_points = [entry_points] if isinstance(entry_points, EntryPoint) else entry_points

            for entry_point in entry_points:
                model_type = entry_point.route.model_type.value
                behavior = entry_point.context.behavior.value

                if model_type in self._entry_points.keys():
                    if behavior in self._entry_points[model_type].keys():
                        del self._entry_points[model_type][behavior]

                        if len(self._entry_points[model_type].keys()) == 0:
                            del self._entry_points[model_type]

    def route(self, model_type: ModelType, behavior: EndpointBehavior) -> EntryPoint:
        """
        Return the entrypoint for the provided configurations.

        :param model_type: ModelType, The API model type to interacted with.
        :param behavior: EndpointBehavior, The expected behavior of the endpoint.
        :return: EntryPoint

        :raises: EntrypointNotFoundException

        """

        if model_type.value in self._entry_points.keys():
            if behavior.value in self._entry_points[model_type.value].keys():
                return self._entry_points[model_type.value][behavior.value]

        raise EntrypointNotFoundException(model_name=model_type.value, behavior=behavior.value)
