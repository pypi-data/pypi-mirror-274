from typing import List, Union, Optional, Dict
from transparent_classroom.api.enums import HTTPMethod
from transparent_classroom.api.enums import EndpointBehavior
from transparent_classroom.api.interfaces.fields import InterfaceField, InterfaceFieldSet


class Interface(object):
    """
    API Interface Class

    This object defines the interface for accessing entry points, i.e. necessary
    parameters, headers, etc.

    Attributes:
        method (`HTTPMethod`): The HTTP method to use when making the request.
        behavior (`EndpointBehavior`): The behavior of the endpoint/what it returns.

    """

    def __init__(self,
            method: HTTPMethod,
            behavior: EndpointBehavior,
            headers: Optional[Union[InterfaceField, List[InterfaceField], InterfaceFieldSet]] = None,
            parameters: Optional[Union[InterfaceField, List[InterfaceField], InterfaceFieldSet]] = None) -> None:
        """
        API Interface Constructor

        :param method: HTTPMethod, The HTTP method to use when making the request.
        :param behavior: EndpointBehavior, The behavior of the endpoint/what it returns.
        :param headers: Optional[Union[InterfaceField, List[InterfaceField], InterfaceFieldSet]],
            Headers to include with the request.
        :param parameters: Optional[Union[InterfaceField, List[InterfaceField], InterfaceFieldSet]],
            Parameters to include with the request.

        """

        self.method = method
        self.behavior = behavior
        self._headers = headers if isinstance(headers, InterfaceFieldSet) else InterfaceFieldSet(fields=headers)
        self._parameters = parameters if isinstance(parameters, InterfaceFieldSet) else InterfaceFieldSet(fields=parameters)

    def headers(self) -> List[InterfaceField]:
        """
        Get the headers of the request.

        :return: List[InterfaceField]

        """

        return self._headers.to_list()

    def add_headers(self, headers: Union[InterfaceField, List[InterfaceField], InterfaceFieldSet]) -> None:
        """
        Add the specified header(s) to the headers included in the request.

        :param headers: Union[InterfaceField, List[InterfaceField], InterfaceFieldSet],
            The headers to add to the request.
        :return: None

        """

        self._headers.add(fields=headers)

    def remove_headers(
            self,
            headers: Union[InterfaceField, str, List[InterfaceField], List[str], InterfaceFieldSet]) -> None:
        """
        Remove the specified headers from the interface.

        :param headers: Union[InterfaceField, str, List[InterfaceField], List[str], InterfaceFieldSet],
            The headers to remove from the request.
        :return: None

        """

        self._headers.remove(fields=headers)

    def parameters(self) -> List[InterfaceField]:
        """
        Get all the parameters of the request.

        :return: Union[List[Parameter], Dict]

        """

        return self._parameters.to_list()

    def add_parameters(self, parameters: Union[InterfaceField, List[InterfaceField], InterfaceFieldSet]) -> None:
        """
        Add the parameters to the interface.

        :param parameters: Union[InterfaceField, List[InterfaceField], InterfaceFieldSet], The
            parameters to add to the request.
        :return: None

        """

        self._parameters.add(fields=parameters)

    def remove_parameters(
            self,
            parameters: Union[InterfaceField, str, List[InterfaceField], List[str], InterfaceFieldSet]) -> None:
        """
        Remove the parameter(s) from the request.

        :param parameters: Union[InterfaceField, str, List[InterfaceField], List[str], InterfaceFieldSet],
            The parameters to remove from the request.
        :return: None

        """

        self._parameters.remove(fields=parameters)

    def validate(self, headers: Dict, parameters: Dict) -> Dict:
        """
        Validate the provided parameters against the fields registered with the interface.

        :param headers: Dict, The parameters to validate.
        :param parameters: Dict, The parameters to validate.
        :return: Dict

        """

        headers = self._headers.validate(bindings=headers)
        parameters = self._parameters.validate(bindings=parameters)
        return {"headers": headers, "parameters": parameters}

    @property
    def method(self) -> HTTPMethod:
        """
        Get the HTTP method used for making the request.

        :return: HTTPMethod

        """

        return self._method

    @method.setter
    def method(self, value: HTTPMethod) -> None:
        """
        Set the HTTP method to use when making the request.

        :param value: HTTPMethod, The method to assign.
        :return: None

        """

        self._method = value

    @property
    def behavior(self) -> EndpointBehavior:
        """
        Get the expected endpoint behavior.

        :return: EndpointBehavior

        """

        return self._behavior

    @behavior.setter
    def behavior(self, value: EndpointBehavior) -> None:
        """
        Set the expected behavior of the endpoint.

        :param value: EndpointBehavior, The expected behavior of the endpoint to assign.
        :return: None

        """

        self._behavior = value
