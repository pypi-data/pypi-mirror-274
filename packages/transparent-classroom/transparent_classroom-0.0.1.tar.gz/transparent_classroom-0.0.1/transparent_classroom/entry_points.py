from transparent_classroom import routes
from transparent_classroom import interfaces
from transparent_classroom.api.entry_points import EntryPoint


# Authentication entry points
AUTH_ENTRY_POINT = EntryPoint(
    name="Authentication Entry Point",
    route=routes.AUTHENTICATE_USER_ROUTE,
    interface=interfaces.AUTH_INTERFACE
)

# Entry point(s) for interacting with the activity object
LIST_ACTIVITIES_ENTRY_POINT = EntryPoint(
    name="List Activities Entry Point",
    route=routes.LIST_ACTIVITIES_ROUTE,
    interface=interfaces.LIST_ACTIVITIES_INTERFACE
)

# Entry point(s) for interacting with the child object
LIST_CHILDREN_ENTRY_POINT = EntryPoint(
    name="List Children Entry Point",
    route=routes.LIST_CHILDREN_ROUTE,
    interface=interfaces.LIST_CHILDREN_INTERFACE
)
GET_CHILD_ENTRY_POINT = EntryPoint(
    name="Get Child Entry Point",
    route=routes.GET_CHILD_ROUTE,
    interface=interfaces.GET_CHILD_INTERFACE
)
UPDATE_CHILD_ENTRY_POINT = EntryPoint(
    name="Update Child Entry Point",
    route=routes.UPDATE_CHILD_ROUTE,
    interface=interfaces.UPDATE_CHILD_INTERFACE
)

# Entry point(s) for interacting with the classroom object
LIST_CLASSROOMS_ENTRY_POINT = EntryPoint(
    name="List Classrooms Entry Point",
    route=routes.LIST_CLASSROOMS_ROUTE,
    interface=interfaces.LIST_CLASSROOMS_INTERFACE
)

# Entry point(s) for interacting with the conference report object
LIST_CONFERENCE_REPORTS_ENTRY_POINT = EntryPoint(
    name="List Conference Reports Entry Point",
    route=routes.LIST_CONFERENCE_REPORTS_ROUTE,
    interface=interfaces.LIST_CONFERENCE_REPORTS_INTERFACE
)

# Entry point(s) for interacting with the event object
LIST_EVENTS_ENTRY_POINT = EntryPoint(
    name="Get Events Entry Point",
    route=routes.LIST_EVENTS_ROUTE,
    interface=interfaces.LIST_EVENTS_INTERFACE
)

# Entry point(s) for interacting with the form object
LIST_FORMS_ENTRY_POINT = EntryPoint(
    name="List Forms Entry Point",
    route=routes.LIST_FORMS_ROUTE,
    interface=interfaces.LIST_FORMS_INTERFACE
)
GET_FORM_ENTRY_POINT = EntryPoint(
    name="Get Form Entry Point",
    route=routes.GET_FORM_ROUTE,
    interface=interfaces.GET_FORM_INTERFACE
)

# Entry point(s) for interacting with the form template object
LIST_FORM_TEMPLATES_ENTRY_POINT = EntryPoint(
    name="List Form Templates Entry Point",
    route=routes.LIST_FORM_TEMPLATES_ROUTE,
    interface=interfaces.LIST_FORM_TEMPLATES_INTERFACE
)

# Entry point(s) for interacting with the lesson set object
GET_LESSON_SET_ENTRY_POINT = EntryPoint(
    name="Get Lesson Set Entry Point",
    route=routes.GET_LESSON_SET_ROUTE,
    interface=interfaces.GET_LESSON_SET_INTERFACE
)

# Entry point(s) for interacting with the level object
LIST_LEVELS_ENTRY_POINT = EntryPoint(
    name="List Levels Entry Point",
    route=routes.LIST_LEVELS_ROUTE,
    interface=interfaces.LIST_LEVELS_INTERFACE
)
LIST_FILTERED_LEVELS_ENTRY_POINT = EntryPoint(
    name="List Filtered Levels Entry Point",
    route=routes.LIST_FILTERED_LEVELS_ROUTE,
    interface=interfaces.LIST_FILTERED_LEVELS_INTERFACE
)

# Entry point(s) for interacting with the online application object
LIST_ONLINE_APPLICATIONS_ENTRY_POINT = EntryPoint(
    name="List Online Applications Entry Point",
    route=routes.LIST_ONLINE_APPLICATIONS_ROUTE,
    interface=interfaces.LIST_ONLINE_APPLICATIONS_INTERFACE
)
GET_ONLINE_APPLICATION_ENTRY_POINT = EntryPoint(
    name="Get Online Application Entry Point",
    route=routes.GET_ONLINE_APPLICATION_ROUTE,
    interface=interfaces.GET_ONLINE_APPLICATION_INTERFACE
)
SUBMIT_ONLINE_APPLICATION_ENTRY_POINT = EntryPoint(
    name="Submit Online Application Entry Point",
    route=routes.SUBMIT_ONLINE_APPLICATION_ROUTE,
    interface=interfaces.SUBMIT_ONLINE_APPLICATION_INTERFACE
)
ACCEPT_ONLINE_APPLICATION_ENTRY_POINT = EntryPoint(
    name="Accept Online Application Entry Point",
    route=routes.ACCEPT_ONLINE_APPLICATION_ROUTE,
    interface=interfaces.ACCEPT_ONLINE_APPLICATION_INTERFACE
)

# Entry point(s) for interacting with the school object
LIST_SCHOOLS_ENTRY_POINT = EntryPoint(
    name="List Schools Entry Point",
    route=routes.LIST_SCHOOLS_ROUTE,
    interface=interfaces.LIST_SCHOOLS_INTERFACE
)

# Entry point(s) for interacting with the session object
LIST_SESSIONS_ENTRY_POINT = EntryPoint(
    name="List Sessions Entry Point",
    route=routes.LIST_SESSIONS_ROUTE,
    interface=interfaces.LIST_SESSIONS_INTERFACE
)

# Entry point(s) for interacting with the user object
LIST_USERS_ENTRY_POINT = EntryPoint(
    name="List Users Entry Point",
    route=routes.LIST_USERS_ROUTE,
    interface=interfaces.LIST_USERS_INTERFACE
)
GET_USER_ENTRY_POINT = EntryPoint(
    name="Get User Entry Point",
    route=routes.GET_USER_ROUTE,
    interface=interfaces.GET_USER_INTERFACE
)
