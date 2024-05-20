class EntrypointNotFoundException(Exception):
    """
    Entrypoint Not Found Exception Class

    Attributes:


    """

    def __init__(self, model_name: str, behavior: str) -> None:
        """
        Entrypoint Not Found Exception Constructor

        :param model_name: str, The name of the model that was not
            found in the API.
        :param behavior: str, The expected behavior of the endpoint.
        :return: None

        """

        super().__init__(f"`{behavior}: {model_name}` Entrypoint Not Found in API.")


class EndpointException(Exception):
    """
    Endpoint Exception Class

    Attributes:


    """

    def __init__(self, title: str, status: int, detail: str) -> None:
        """
        Endpoint Exception Constructor

        :param title: str, The title of the exception.
        :param status: int, Status code of the error response.
        :param detail: str, Details from the endpoint describing the error.
        :return: None

        """

        self.title = title
        self.status = status
        self.detail = detail

    def __str__(self) -> str:
        """
        String description of the exception.

        :return: str

        """

        return f"{self.status} Error {self.title}: {self.detail}"
