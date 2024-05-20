from transparent_classroom import models
from typing import Dict, List, Generic, TypeVar, Union, Type


_J = TypeVar('_J', bound=models.JSONModel)


class Deserializer(Generic[_J]):
    """
    Abstract Base Class for JSON Deserialization

    Attributes:


    """

    def __init__(self, cls: Type[_J]) -> None:
        """
        Deserializer Constructor

        :param cls: Type, The model type to deserialize.
        :return: None

        """

        self._cls = cls

    def deserialize(self, data: Dict) -> _J:
        """
        Method for deserializing the provided object data into the associated object.

        :param data: Dict, The object to serialize.
        :return: _J

        """

        return self._cls.from_dict(data=data)

    def batch(self, data: Union[Dict, List[Dict]]) -> List[_J]:
        """
        Batch deserialize the objects.

        :param data: Union[Dict, List[Dict]], The object to deserialize.
        :return: List[_J]

        """

        deserialized_objects = []
        data = data if isinstance(data, list) else [data]

        for obj_data in data:
            deserialized_objects.append(self.deserialize(data=obj_data))

        return deserialized_objects


class ActivityDeserializer(Deserializer[models.Activity]):
    """
    Activity Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into activity objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Activity Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Activity)


class ChildDeserializer(Deserializer[models.Child]):
    """
    Child Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into child objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Child Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Child)


class ClassroomDeserializer(Deserializer[models.Classroom]):
    """
    Classroom Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into classroom objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Classroom Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Classroom)


class WidgetDeserializer(Deserializer[models.Widget]):
    """
    Widget Deserializer Class

    This class will deserialize the Widget data from a form template API response and
    convert it into a Widget object.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Widget Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Widget)

    def deserialize(self, data: Dict) -> models.Widget:
        """
        Method for deserializing the provided object data into a Widget object.

        :param data: Dict, The object to serialize.
        :return: models.Widget

        """

        return models.Widget(attributes=data)


class FormTemplateDeserializer(Deserializer[models.FormTemplate]):
    """
    Form Template Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into form template objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Form Template Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.FormTemplate)

    def deserialize(self, data: Dict) -> models.FormTemplate:
        """
        Method for deserializing the provided object data into a form template object.

        :param data: Dict, The object to serialize.
        :return: models.FormTemplate

        """

        if "widgets" in data:
            data['widgets'] = WidgetDeserializer().batch(data=data['widgets'])

        return super().deserialize(data=data)


class ConferenceReportDeserializer(Deserializer[models.ConferenceReport]):
    """
    Conference Report Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into conference report objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Conference Report Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.ConferenceReport)

    def deserialize(self, data: Dict) -> models.ConferenceReport:
        """
        Method for deserializing the provided object data into a conference report object.

        :param data: Dict, The object to serialize.
        :return: models.Form

        """

        formatted_data = {
            "id": data.get("id", None),
            "name": data.get("name", None),
            "child_id": data.get("child_id", None),
            "widgets": data.get("data", [])
        }

        formatted_data['widgets'] = WidgetDeserializer().batch(data=formatted_data['widgets'])
        return super().deserialize(data=formatted_data)


class EventDeserializer(Deserializer[models.Event]):
    """
    Event Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into event objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Event Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Event)


class FormDeserializer(Deserializer[models.Form]):
    """
    Form Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into form (response) objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Form (Response) Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Form)

    def deserialize(self, data: Dict) -> models.ConferenceReport:
        """
        Method for deserializing the provided object data into a conference report object.

        :param data: Dict, The object to serialize.
        :return: models.ConferenceReport

        """

        fields = []

        if 'fields' in data.keys():
            for name in data['fields'].keys():
                fields.append({
                    'name': name,
                    'value': data['fields'][name]
                })

        data['fields'] = WidgetDeserializer().batch(data=fields)
        return super().deserialize(data=data)


class LessonDeserializer(Deserializer[models.Lesson]):
    """
    Lesson Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into lesson objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Lesson Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Lesson)

    def deserialize(self, data: Dict) -> models.Lesson:
        """
        Method for deserializing the provided object data into a lesson object.

        :param data: Dict, The object to serialize.
        :return: models.Lesson

        """

        data['photo'] = data.pop('profile_photo', None)
        data['material'] = data.pop('material_name', None)

        if 'children' in data.keys():
            del data['children']

        return super().deserialize(data=data)


class GroupDeserializer(Deserializer[models.Group]):
    """
    Group Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into group objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Group Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Group)

    def deserialize(self, data: Dict) -> models.Group:
        """
        Method for deserializing the provided object data into a group object.

        :param data: Dict, The object to serialize.
        :return: models.Group

        """

        data['subgroups'] = GroupDeserializer().batch(data=data.pop('children'))
        data['lessons'] = LessonDeserializer().batch(data=data.pop('lessons', []))
        return super().deserialize(data=data)


class AreaDeserializer(Deserializer[models.Area]):
    """
    Area Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into area objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Area Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Area)

    def deserialize(self, data: Dict) -> models.Area:
        """
        Method for deserializing the provided object data into an area object.

        id (`int`): The Transparent Classroom object id of the lesson set.
        archetype_id (`int`): The id of the archetype.
        name (`str`): The name of the lesson, group, or material being worked.
        type (`str`): The type of the archetype object (group, lesson, etc.)
        description (`str`): The description of the object.
        groups (`List[Group]`): The groups defining this lesson set area.

        :param data: Dict, The object to serialize.
        :return: models.Area

        """

        data['groups'] = GroupDeserializer().batch(data=data.pop('children'))
        return super().deserialize(data=data)


class LessonSetDeserializer(Deserializer[models.LessonSet]):
    """
    Lesson Set Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into lesson set objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Lesson Set Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.LessonSet)

    def deserialize(self, data: Dict) -> models.LessonSet:
        """
        Method for deserializing the provided object data into a lesson set object.

        :param data: Dict, The object to serialize.
        :return: models.LessonSet

        """

        scales = []

        if 'scales' in data.keys():
            for k, v in data['scales'].items():
                scales.append(models.Scale(name=k, values=v))

        data['scales'] = scales
        data['areas'] = AreaDeserializer().batch(data=data.pop('children'))
        return super().deserialize(data=data)


class LevelDeserializer(Deserializer[models.Level]):
    """
    Level Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into level objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Level Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Level)


class OnlineApplicationDeserializer(Deserializer[models.OnlineApplication]):
    """
    Online Application Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into online application objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Online Application Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.OnlineApplication)

    def deserialize(self, data: Dict) -> models.OnlineApplication:
        """
        Method for deserializing the provided object data into a conference report object.

        :param data: Dict, The object to serialize.
        :return: models.OnlineApplication

        """

        fields = []

        if 'fields' in data.keys():
            for name in data['fields'].keys():
                fields.append({
                    'name': name,
                    'value': data['fields'][name]
                })

        data['fields'] = WidgetDeserializer().batch(data=fields)
        return super().deserialize(data=data)


class SchoolDeserializer(Deserializer[models.School]):
    """
    School Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into school objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        School Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.School)


class SessionDeserializer(Deserializer[models.Session]):
    """
    Session Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into session objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Session Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Session)


class UserDeserializer(Deserializer[models.User]):
    """
    User Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into user objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        User Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.User)


class AuthDeserializer(Deserializer[models.Auth]):
    """
    Auth Deserializer Class

    This class will deserialize the object data from an API response and convert
    it into auth objects.

    Attributes:


    """

    def __init__(self) -> None:
        """
        Auth Deserializer Constructor

        :return: None

        """

        super().__init__(cls=models.Auth)

    def deserialize(self, data: Dict) -> models.Auth:
        """
        Method for deserializing the provided object data into an auth object.

        :param data: Dict, The object to serialize.
        :return: models.Auth

        """

        auth_data, user_data = {}, {}
        auth_properties = ["school_id", "api_token", "push_tokens", "push_enabled"]

        for k, v in data.items():
            if k in auth_properties:
                auth_data[k] = v
            else:
                user_data[k] = v

        user_deserializer = UserDeserializer()
        auth_data["user"] = user_deserializer.deserialize(data=user_data)
        return super().deserialize(data=auth_data)
