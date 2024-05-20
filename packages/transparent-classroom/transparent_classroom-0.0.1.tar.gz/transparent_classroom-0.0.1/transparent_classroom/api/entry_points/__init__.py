from transparent_classroom.api.enums import ModelType
from transparent_classroom.api.routing.routes import Route
from transparent_classroom.api.interfaces import Interface


class EntryPoint(object):
    """
    Entry Point Class

    Attributes:
        name (`str`): The name of the entry point.
        route (`Route`): The route to the entrypoint.
        interface (`Interface`): The interface defining how to make requests to the
            API entry point.

    """

    def __init__(self, name: str, route: Route, interface: Interface) -> None:
        """
        Entry Point Constructor

        :param name: str, The name of the entry point.
        :param route: Route, The route that this entry point is associated with.
        :param interface: Interface, The interface defining how to make requests to the
            API entry point.
        :return: None

        """

        self.name = name
        self.route = route
        self.interface = interface

    @property
    def name(self) -> str:
        """
        The name of the route.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the entry point.

        :param value: str, The name of the entry point to set.
        :return: None

        """

        self._name = value

    @property
    def route(self) -> Route:
        """
        The route to the entry point.

        :return: Route

        """

        return self._route

    @route.setter
    def route(self, value: Route) -> None:
        """
        Set the route to the entry point.

        :param value: Route, The route to set.
        :return: None

        """

        self._route = value

    @property
    def interface(self) -> Interface:
        """
        The interface defining how to make requests to the API entry point.

        :return: EntryPointContext

        """

        return self._interface

    @interface.setter
    def interface(self, value: Interface) -> None:
        """
        Set the interface defining how to make requests to the API entry point.

        :param value: Interface, The API interface to set.
        :return: None

        """

        self._interface = value

    @property
    def model_type(self) -> ModelType:
        """
        The model associated with the entry point.

        :return: ModelType

        """

        return self.route.model_type
