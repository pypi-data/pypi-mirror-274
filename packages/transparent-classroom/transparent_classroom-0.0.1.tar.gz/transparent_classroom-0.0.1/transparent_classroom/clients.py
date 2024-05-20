import requests
import itertools
from datetime import date, datetime
from transparent_classroom import apis
from requests.auth import HTTPBasicAuth
from transparent_classroom import models
from transparent_classroom.api.enums import HTTPMethod
from typing import Optional, List, Dict, Union, TypeVar
from transparent_classroom.api.entry_points import EntryPoint
from transparent_classroom.models import deserializers
from transparent_classroom.api.exceptions import EndpointException
from transparent_classroom.api.enums import ModelType, EndpointBehavior


M = TypeVar('M', bound=Union[models.Model])


def convert_date(date_str: Union[str, date, datetime]) -> date:
    """
    The string to convert.

    :param date_str: Union[str, date, datetime], The string to convert into a date.
    :return: date

    """

    if (date_str is not None) and isinstance(date_str, str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    return date_str


class Client(object):
    """
    Client Class

    Attributes:
        email (`str`): The email of the account to use for authenticating
            to Transparent Classroom.
        password (`str`): The password of the account to use for
            authenticating to Transparent Classroom.
        host (`str`): The root url of the host of the API.
        masquerade_id (`int`): As an admin, you can act as another user
            by setting this header to the user's ID.
        school_id (`int`): As a network admin, you can act on behalf of a
            school in your network by setting this header to the school's ID.

    """

    """
    The default Transparent Classroom host address
    
    """
    __DEFAULT_HOST = "https://www.transparentclassroom.com"

    def __init__(
            self,
            email: str,
            password: str,
            host: Optional[str] = None,
            masquerade_id: Optional[int] = None,
            school_id: Optional[int] = None) -> None:
        """
        Transparent Classroom Client Constructor

        :param email: str, The email of the account to use for authenticating
            to Transparent Classroom.
        :param password: str, The password of the account to use for
            authenticating to Transparent Classroom.
        :param masquerade_id: Optional[int], As an admin, you can act as another
            user by setting this header to the user's ID.
        :param school_id: Optional[int], As a network admin, you can act on behalf
            of a school in your network by setting this header to the school's ID.
        :param host: Optional[str], The root url of the host of the API.
        :return: None

        """

        self.__token = None
        self.email = email
        self.password = password
        self.__api = apis.api
        self.masquerade_id = masquerade_id
        self.school_id = school_id
        self.host = host

    def __access(self, parameters: Dict, deserializer: deserializers.Deserializer, parse_mode: str = "deserialize") -> Union[M, List[M]]:
        """
        Generalized accessor for the object data.

        :param parameters: Dict, The parameters to use when making the request.
        :param deserializer: deserializers.Deserializer, The deserializer to use
            when parsing the response data.
        :param parse_mode: str, The deserialization method to use for parsing
            (deserialize, batch).
        :return: Union[M, List[M]]

        """

        response = self.__submit(**parameters)
        data = response.json()

        if hasattr(data, "keys") and "errors" in data.keys():
            raise EndpointException(**data["errors"][0])

        return deserializer.__getattribute__(parse_mode)(data=data)

    def __get(self, parameters: Dict, deserializer: deserializers.Deserializer, mode: str = "get") -> Union[M, List[M]]:
        """
        Retrieve the object data.

        :param parameters: Dict, The parameters to use when making the request.
        :param deserializer: deserializers.Deserializer, The deserializer to use
            when parsing the response data.
        :param mode: str, The accessor mode to use when making the request.
        :return: Union[M, List[M]]

        """

        if ("behavior" not in parameters.keys()) or (parameters["behavior"] is None):
            parameters["behavior"] = EndpointBehavior.SHOW

        parse_mode = "batch" if mode == "batch" else "deserialize"
        return self.__access(parameters=parameters, deserializer=deserializer, parse_mode=parse_mode)

    def __batch(self, parameters: Dict, deserializer: deserializers.Deserializer, paginated: bool = False) -> List[M]:
        """
        Convenience method for batch get requests

        :param parameters: Dict, The parameters to use when making the request.
        :param deserializer: deserializers.Deserializer, The deserializer to use
            when parsing the response data.
        :param paginated: bool, Flag indicating whether the endpoint is paginated.
        :return: List[M]

        """

        max_per_page = 1000
        record_sets, done = [], False

        if ("behavior" not in parameters.keys()) or (parameters["behavior"] is None):
            parameters["behavior"] = EndpointBehavior.LIST

        if paginated:
            parameters["parameters"]["page"] = 1
            parameters["parameters"]["per_page"] = max_per_page

        while not done:
            record_set = self.__get(parameters=parameters, deserializer=deserializer, mode="batch")

            if (len(record_set) < max_per_page) or (not paginated):
                done = True
            else:
                parameters["parameters"]["page"] += 1

            record_sets.append(record_set)

        return list(itertools.chain.from_iterable(record_sets))

    @staticmethod
    def __request(context: Dict) -> requests.Response:
        """
        Send the request to the API.

        :param context: Dict, The dictionary containing the headers, parameters, and
            other request metadata to include with the request.
        :return: requests.Response

        """

        url = context["url"]
        kwargs = {
            "headers": context["headers"],
            "params": context["parameters"]
        }

        if ("email" in kwargs["params"]) and ("password" in kwargs["params"]):
            email = kwargs["params"]["email"]
            password = kwargs["params"]["password"]
            kwargs["auth"] = HTTPBasicAuth(email, password)
            del kwargs["params"]["email"]
            del kwargs["params"]["password"]

        if context["method"] == HTTPMethod.POST:
            return requests.post(url, **kwargs)
        elif context["method"] == HTTPMethod.PUT:
            return requests.put(url, **kwargs)
        else:
            return requests.get(url, **kwargs)

    def __get_context(self, entry_point: EntryPoint, parameters: Dict, route_parameters: Dict) -> Dict:
        """
        Validate and return the validated context data for the entry point.

        :param entry_point: EntryPoint, The entry point of the API.
        :param parameters: Dict, The parameters to send to the entry point (Transparent Classroom).
        :param route_parameters: Dict, The route parameters used to build/customize the route.
        :return: Dict

        """

        if ("model_name" not in route_parameters.keys()) or (route_parameters["model_name"] is None):
            route_parameters["model_name"] = entry_point.model_type.value

        context = entry_point.interface.validate(headers=self.headers, parameters=parameters)
        context["url"] = "/".join([self.host, entry_point.route.apply(**route_parameters)])
        context["method"] = entry_point.interface.method
        return context

    def __submit(
            self,
            model_type: ModelType,
            behavior: EndpointBehavior,
            parameters: Dict,
            route_parameters: Optional[Dict] = None) -> requests.Response:
        """
        Route the kwargs to the relevant entrypoint, build the request, and submit
        the request to the API.

        :param model_type: ModelType, The API model type to interacted with.
        :param behavior: EndpointBehavior, The expected behavior of the endpoint.
        :param parameters: Dict, The params to provide to the entry point.
        :param route_parameters: Optional[Dict], The params to provide for updating the route.
        :return: requests.Response

        """

        if (self.token is None) and (model_type is not ModelType.AUTHENTICATE):
            self.authenticate()

        entry_point = self.__api.route(model_type=model_type, behavior=behavior)
        context = self.__get_context(entry_point=entry_point, parameters=parameters, route_parameters=route_parameters)
        return self.__request(context=context)

    def authenticate(self) -> None:
        """
        Authenticate the client with Transparent Classroom.

        :return: None

        """

        self.__auth = self.__get(
            parameters={
                "model_type": ModelType.AUTHENTICATE,
                "parameters": {
                    "email": self.email,
                    "password": self.password
                },
                "route_parameters": {}
            },
            deserializer=deserializers.AuthDeserializer()
        )
        self.__auth.user = self.get_user(user_id=self.__auth.user.id)

    def get_activities(
            self,
            child_id: Optional[int] = None,
            classroom_id: Optional[int] = None,
            only_photos: Optional[bool] = False,
            only_portfolio: Optional[bool] = False,
            after: Optional[Union[str, date]] = None,
            before: Optional[Union[str, date]] = None) -> List[models.Activity]:
        """
        Get all the activities (possibly filtered by child or classroom).

        :param child_id: Optional[int], The id of the child to show observations,
            presentations, and/or photos for.
        :param classroom_id: Optional[int], The id of the classroom to show observations,
            presentations, and/or photos for.
        :param only_photos: Optional[bool], Flag indicating that only photos should
            be returned.
        :param only_portfolio: Optional[bool], Flag indicating that only portfolio items
            should be returned.
        :param after: Optional[Union[str, date]], Filter parameter to only return records
            on/after this date. (format: 2016-05-01)
        :param before: Optional[Union[str, date]], Filter parameter to only return records
            on/before this date. (format: 2016-05-01)
        :return: List[models.Activity]

        :raises: ValueError

        """

        if (child_id is None) and (classroom_id is None):
            raise ValueError("Either a child_id or classroom_id value needs to be provided.")

        return self.__batch(
            parameters={
                "model_type": ModelType.ACTIVITY,
                "parameters": {
                    "child_id": child_id,
                    "classroom_id": classroom_id,
                    "only_photos": "true" if only_photos else "false",
                    "only_portfolio": "true" if only_portfolio else "false",
                    "date_start": convert_date(date_str=after),
                    "date_end": convert_date(date_str=before)
                },
                "route_parameters": {}
            },
            deserializer=deserializers.ActivityDeserializer(),
            paginated=True
        )

    def get_child(self, child_id: int, as_of: Optional[Union[str, date]] = None) -> models.Child:
        """
        Get the specified child data.

        :param child_id: int, The id of the child to get the data for.
        :param as_of: Optional[Union[str, date]], If specified, shows child fields as
            of this date
        :return: models.Child

        """

        return self.__get(
            parameters={
                "model_type": ModelType.CHILDREN,
                "parameters": {
                    "as_of": convert_date(date_str=as_of)
                },
                "route_parameters": {
                    "object_id": child_id
                }
            },
            deserializer=deserializers.ChildDeserializer()
        )

    def get_children(
            self,
            classroom_id: Optional[int] = None,
            session_id: Optional[int] = None,
            only_current: Optional[bool] = False) -> List[models.Child]:
        """
        Get all the children (possibly filtered by classroom, session, and/or recency).

        :param classroom_id: Optional[int], The id of the classroom to use when filtering
            children to show. Required for teachers, optional for admin staff.
        :param session_id: Optional[int], The id of the session to filter the children by.
            Will use the current session as the filter, if None provided.
        :param only_current: Optional[bool], Flag indicating that only currently enrolled
            children will be returned.
        :return: List[models.Child]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.CHILDREN,
                "parameters": {
                    "classroom_id": classroom_id,
                    "session_id": session_id,
                    "only_current": "true" if only_current else "false"
                },
                "route_parameters": {}
            },
            deserializer=deserializers.ChildDeserializer()
        )

    def get_classrooms(self, show_inactive: Optional[bool] = False) -> List[models.Classroom]:
        """
        Get all the available/registered classrooms at the school.

        :param show_inactive: Optional[bool], Flag indicating whether inactive classrooms
            should be returned in the response.
        :return: List[models.Classroom]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.CLASSROOMS,
                "parameters": {
                    "show_inactive": "true" if show_inactive else "false"
                },
                "route_parameters": {}
            },
            deserializer=deserializers.ClassroomDeserializer()
        )

    def get_conference_reports(
            self,
            child_id: Optional[int] = None,
            after: Optional[Union[str, date]] = None,
            before: Optional[Union[str, date]] = None) -> List[models.ConferenceReport]:
        """
        Get all the available/registered classrooms at the school.

        :param child_id: Optional[int], The id of the child to filter conference reports for.
        :param after: Optional[Union[str, date]], Only show reports created on or after date
            (format: 2016-05-01).
        :param before: Optional[Union[str, date]], Only show reports created on or before date
            (format: 2016-04-01).
        :return: List[models.ConferenceReport]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.CONFERENCE_REPORTS,
                "parameters": {
                    "child_id": child_id,
                    "created_after": convert_date(date_str=after),
                    "created_before": convert_date(date_str=before)
                },
                "route_parameters": {}
            },
            deserializer=deserializers.ConferenceReportDeserializer(),
            paginated=True
        )

    def get_events(self, child_id: int, start_date: Union[str, date], end_date: Union[str, date]) -> List[models.Event]:
        """
        Get the specified child's events for the provided date range.

        :param child_id: int, The id of the child to get events for.
        :param start_date: Union[str, date], The start date to use when filtering for events.
        :param end_date: Union[str, date], The end date to use when filtering for events.
        :return: List[models.Event]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.EVENTS,
                "parameters": {
                    "child_id": child_id,
                    "date_start": convert_date(date_str=start_date),
                    "date_end": convert_date(date_str=end_date)
                },
                "route_parameters": {}
            },
            deserializer=deserializers.EventDeserializer(),
            paginated=False
        )

    def get_form(self, form_id: int) -> models.Form:
        """
        Get the specified form instance's response data (i.e. an individual response
        to a form template).

        :param form_id: int, The id of the form response to get.
        :return: models.Form

        """

        return self.__get(
            parameters={
                "model_type": ModelType.FORMS,
                "parameters": {},
                "route_parameters": {
                    "object_id": form_id
                }
            },
            deserializer=deserializers.FormDeserializer()
        )

    def get_forms(
            self,
            form_template_id: Optional[int] = None,
            child_id: Optional[int] = None,
            after: Optional[Union[str, date]] = None,
            before: Optional[Union[str, date]] = None) -> List[models.Form]:
        """
        Get all the form responses with the optional filtering.

        :param form_template_id: Optional[int], The id of the form template/type to filter by.
        :param child_id: Optional[int], The id of the child to filter form responses by.
        :param after: Optional[Union[str, date]], Filter to only form responses created on or
            after a certain date.
        :param before: Optional[Union[str, date]], Filter to only form responses created on or
            before a certain date.
        :return: List[models.Form]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.FORMS,
                "parameters": {
                    "form_template_id": form_template_id,
                    "child_id": child_id,
                    "created_after": convert_date(date_str=after),
                    "created_before": convert_date(date_str=before)
                },
                "route_parameters": {}
            },
            deserializer=deserializers.FormDeserializer()
        )

    def get_form_templates(self) -> List[models.FormTemplate]:
        """
        Get all the form templates (their metadata, widgets, etc.).

        :return: List[models.FormTemplate]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.FORM_TEMPLATES,
                "parameters": {},
                "route_parameters": {}
            },
            deserializer=deserializers.FormTemplateDeserializer()
        )

    def get_lesson_set(self, lesson_set_id: int, format: Optional[str] = "short") -> models.LessonSet:
        """
        Get the lesson set and all the associated lessons in the lesson set.

        :param lesson_set_id: int, The id of the lesson set to get.
        :param format: Optional[str], Format of the lesson set description. Long will include
            photos and descriptions, defaults to short [long, short].
        :return: models.LessonSet

        """

        return self.__get(
            parameters={
                "model_type": ModelType.LESSON_SETS,
                "parameters": {
                    "format": format
                },
                "route_parameters": {
                    "object_id": lesson_set_id
                }
            },
            deserializer=deserializers.LessonSetDeserializer()
        )

    def get_levels(self, child_id: int, lesson_set_id: Optional[int] = None) -> List[models.Level]:
        """
        Get the levels of the student filtered by the specified lesson set. Note, this
        does not include the date of the lesson (populates them with null), because it
        includes lessons of all status (those given and not given).

        :param child_id: int, The id of the child to get the lesson set levels for.
        :param lesson_set_id: Optional[int], The id of the lesson set to get the levels for.
        :return: List[models.Level]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.LEVELS,
                "behavior": EndpointBehavior.SHOW_ALL,
                "parameters": {
                    "child_id": child_id,
                    "lesson_set_id": lesson_set_id
                },
                "route_parameters": {}
            },
            deserializer=deserializers.LevelDeserializer(),
            paginated=True
        )

    def get_levels_in_date_range(
            self,
            child_id: int,
            start_date: Union[str, date],
            end_date: Union[str, date]) -> List[models.Level]:
        """
        Get the levels of the student filtered by a date range. Only shows lessons
        that have happened (planned is missing).

        :param child_id: int, The id of the child to get the lesson set levels for.
        :param start_date: Union[str, date], The start date of the date range to use
            when filtering lesson set levels.
        :param end_date: Union[str, date], The end date of the date range to use when
            filtering lesson set levels.
        :return: List[models.Level]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.LEVELS,
                "behavior": EndpointBehavior.SHOW_FILTERED,
                "parameters": {
                    "child_id": child_id,
                    "date_start": convert_date(date_str=start_date),
                    "date_end": convert_date(date_str=end_date)
                },
                "route_parameters": {}
            },
            deserializer=deserializers.LevelDeserializer()
        )

    def get_online_application(self, online_application_id: int) -> models.OnlineApplication:
        """
        Get the form data of the specified online application.

        :param online_application_id: int, The id of the online application to get.
        :return: models.OnlineApplication

        """

        return self.__get(
            parameters={
                "model_type": ModelType.ONLINE_APPLICATIONS,
                "parameters": {},
                "route_parameters": {
                    "object_id": online_application_id
                }
            },
            deserializer=deserializers.OnlineApplicationDeserializer()
        )

    def get_online_applications(
            self,
            after: Optional[Union[str, date, datetime]] = None) -> List[models.OnlineApplication]:
        """
        Get all the online application responses (optionally filtered to include all responses
        after the provided created_at datetime value). Listing online applications does not
        populate additional form data fields/widgets (school_id, type, fields).

        :param after: Optional[Union[str, date, datetime]], Filter to only include online
            applications completed on or after the specified date, date-like string, datetime.
        :return: List[models.OnlineApplication]

        """

        after = convert_date(date_str=after)

        if (after is not None) and isinstance(after, date):
            after = datetime(after.year, after.month, after.day)

        return self.__batch(
            parameters={
                "model_type": ModelType.ONLINE_APPLICATIONS,
                "parameters": {
                    "created_at": after
                },
                "route_parameters": {}
            },
            deserializer=deserializers.OnlineApplicationDeserializer()
        )

    def get_schools(self) -> List[models.School]:
        """
        Get all the schools registered within the network on Transparent Classroom.

        :return: List[models.School]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.SCHOOLS,
                "parameters": {},
                "route_parameters": {}
            },
            deserializer=deserializers.SchoolDeserializer()
        )

    def get_sessions(self) -> List[models.Session]:
        """
        Get all the schools registered within the network on Transparent Classroom.

        :return: List[models.Session]

        """

        if (self.roles is not None) and ("admin" not in self.roles):
            raise ValueError("You must be an admin to get the list of sessions.")

        return self.__batch(
            parameters={
                "model_type": ModelType.SESSIONS,
                "parameters": {},
                "route_parameters": {}
            },
            deserializer=deserializers.SessionDeserializer()
        )

    def get_user(self, user_id: int) -> models.User:
        """
        Get the specified user's details.

        :param user_id: int, The id of the user to get.
        :return: models.User

        """

        return self.__get(
            parameters={
                "model_type": ModelType.USERS,
                "parameters": {},
                "route_parameters": {
                    "object_id": user_id
                }
            },
            deserializer=deserializers.UserDeserializer()
        )

    def get_users(self, classroom_id: Optional[int] = None, roles: Optional[List[str]] = None) -> List[models.User]:
        """
        Get all the users in Transparent Classroom (potentially filtered using the available
        method parameters). Listing users does not populate additional user data fields
        (accessible_classroom_ids, default_classroom_id, street, city, postal_code, etc.).

        :param classroom_id: Optional[int], Filter the response to only include users that have
            an affiliation with the specified classroom id (required for teachers).
        :param roles: Optional[List[str]], Filter the response to include users matching any of the
            roles included in the request (teacher, parent, admin, billing_manager, family_member).
        :return: List[models.User]

        """

        return self.__batch(
            parameters={
                "model_type": ModelType.USERS,
                "parameters": {
                    "classroom_id": classroom_id,
                    "roles[]": roles
                },
                "route_parameters": {}
            },
            deserializer=deserializers.UserDeserializer()
        )

    @property
    def email(self) -> str:
        """
        Email accessor method.

        :return: str

        """

        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """
        Email setter method.

        :param value: str, The value to set the email attribute to.
        :return: None

        """

        self.__auth = None
        self._email = value

    @property
    def password(self) -> str:
        """
        Password accessor method.

        :return: str

        """

        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """
        Password setter method.

        :param value: str, The value to set the password attribute to.
        :return: None

        """

        self.__auth = None
        self._password = value

    @property
    def masquerade_id(self) -> int:
        """
        Get the masquerade id.

        :return: int

        """

        return self._masquerade_id

    @masquerade_id.setter
    def masquerade_id(self, value: int) -> None:
        """
        Set the masquerade id (the user id to masquerade as), if the
        provided credentials are associated with an admin account.

        :param value: int, The masquerade id.
        :return: None

        """

        self._masquerade_id = value

    @property
    def school_id(self) -> int:
        """
        Get the school id.

        :return: int

        """

        return self._school_id

    @school_id.setter
    def school_id(self, value: int) -> None:
        """
        As a network admin, you can act on behalf of a school in your
        network by setting this header to the school's ID.

        :param value: int, The school id.
        :return: None

        """

        self._school_id = value

    @property
    def authenticated_user(self) -> models.User:
        """
        The authenticated Transparent Classroom user object.

        :return: models.User

        """

        return None if self.__auth is None else self.__auth.user

    @property
    def token(self) -> str:
        """
        The access token retrieved from Transparent Classroom.

        :return: str

        """

        return None if self.__auth is None else self.__auth.api_token

    @property
    def roles(self) -> List:
        """
        The access roles that the user belongs to.

        :return: List

        """

        return None if self.__auth is None else self.__auth.user.roles

    @property
    def host(self) -> str:
        """
        Get the root host server address of the API.

        :return: str

        """

        return self.__DEFAULT_HOST if self._host is None else self._host

    @host.setter
    def host(self, value: str) -> None:
        """
        Set the API host address.

        :param value: str, The API root host address.
        :return: None

        """

        self._host = self.__DEFAULT_HOST if value is None else value.rstrip("/")

    @property
    def headers(self) -> Dict:
        """
        Get the header values used by the client when making requests.

        :return: Dict

        """

        headers = {
            "X-TransparentClassroomToken": self.token,
            "X-TransparentClassroomMasqueradeId": self.masquerade_id,
            "X-TransparentClassroomSchoolId": self.school_id
        }
        return {k: str(v) if headers[k] is not None else v for k, v in headers.items()}

