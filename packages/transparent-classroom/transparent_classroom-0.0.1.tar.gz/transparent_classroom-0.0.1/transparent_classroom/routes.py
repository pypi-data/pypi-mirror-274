from transparent_classroom.api.enums import ModelType
from transparent_classroom.api.routing.routes import Route
import transparent_classroom.route_components as route_components


# Basic ordering of route components for listing objects
_LIST_OBJECT_ROUTE_COMPONENTS = [
    route_components.API_V1_ROUTE_COMPONENT,
    route_components.MODEL_ROUTE_COMPONENT
]

# Basic ordering of route components for getting a specific object
_GET_OBJECT_ROUTE_COMPONENTS = [
    route_components.API_V1_ROUTE_COMPONENT,
    route_components.MODEL_ROUTE_COMPONENT,
    route_components.OBJECT_ID_ROUTE_COMPONENT
]

# Basic ordering of route components for updating a specific object
_UPDATE_OBJECT_ROUTE_COMPONENTS = _GET_OBJECT_ROUTE_COMPONENTS

# Basic ordering of route components for submitting a specific object
_SUBMIT_OBJECT_ROUTE_COMPONENTS = _LIST_OBJECT_ROUTE_COMPONENTS

# Authentication Routes
AUTHENTICATE_USER_ROUTE = Route(model_type=ModelType.AUTHENTICATE, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Activity Routes
LIST_ACTIVITIES_ROUTE = Route(model_type=ModelType.ACTIVITY, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Children Routes
GET_CHILD_ROUTE = Route(model_type=ModelType.CHILDREN, components=_GET_OBJECT_ROUTE_COMPONENTS)
LIST_CHILDREN_ROUTE = Route(model_type=ModelType.CHILDREN, components=_LIST_OBJECT_ROUTE_COMPONENTS)
UPDATE_CHILD_ROUTE = Route(model_type=ModelType.CHILDREN, components=_UPDATE_OBJECT_ROUTE_COMPONENTS)

# Classrooms Routes
LIST_CLASSROOMS_ROUTE = Route(model_type=ModelType.CLASSROOMS, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Conference Reports Routes
LIST_CONFERENCE_REPORTS_ROUTE = Route(model_type=ModelType.CONFERENCE_REPORTS, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Events Routes
LIST_EVENTS_ROUTE = Route(model_type=ModelType.EVENTS, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Forms Routes
GET_FORM_ROUTE = Route(model_type=ModelType.FORMS, components=_GET_OBJECT_ROUTE_COMPONENTS)
LIST_FORMS_ROUTE = Route(model_type=ModelType.FORMS, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Form Templates Routes
LIST_FORM_TEMPLATES_ROUTE = Route(model_type=ModelType.FORM_TEMPLATES, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Lesson Sets Routes
GET_LESSON_SET_ROUTE = Route(model_type=ModelType.LESSON_SETS, components=_GET_OBJECT_ROUTE_COMPONENTS)

# Levels Routes
LIST_LEVELS_ROUTE = Route(model_type=ModelType.LEVELS, components=_LIST_OBJECT_ROUTE_COMPONENTS)
LIST_FILTERED_LEVELS_ROUTE = Route(
    model_type=ModelType.LEVELS,
    components=_LIST_OBJECT_ROUTE_COMPONENTS + [route_components.FILTER_LEVELS_BY_DATE_ROUTE_COMPONENT]
)

# Online Applications Routes
GET_ONLINE_APPLICATION_ROUTE = Route(
    model_type=ModelType.ONLINE_APPLICATIONS,
    components=_GET_OBJECT_ROUTE_COMPONENTS
)
LIST_ONLINE_APPLICATIONS_ROUTE = Route(
    model_type=ModelType.ONLINE_APPLICATIONS,
    components=_LIST_OBJECT_ROUTE_COMPONENTS
)
SUBMIT_ONLINE_APPLICATION_ROUTE = Route(
    model_type=ModelType.ONLINE_APPLICATIONS,
    components=_SUBMIT_OBJECT_ROUTE_COMPONENTS
)
ACCEPT_ONLINE_APPLICATION_ROUTE = Route(
    model_type=ModelType.ONLINE_APPLICATIONS,
    components=_GET_OBJECT_ROUTE_COMPONENTS + [route_components.ACCEPT_APPLICATION_ROUTE_COMPONENT]
)

# Schools Routes
LIST_SCHOOLS_ROUTE = Route(model_type=ModelType.SCHOOLS, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Sessions Routes
LIST_SESSIONS_ROUTE = Route(model_type=ModelType.SESSIONS, components=_LIST_OBJECT_ROUTE_COMPONENTS)

# Users Routes
GET_USER_ROUTE = Route(model_type=ModelType.USERS, components=_GET_OBJECT_ROUTE_COMPONENTS)
LIST_USERS_ROUTE = Route(model_type=ModelType.USERS, components=_LIST_OBJECT_ROUTE_COMPONENTS)
