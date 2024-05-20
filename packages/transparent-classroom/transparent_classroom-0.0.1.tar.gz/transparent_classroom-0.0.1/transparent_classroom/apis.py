from transparent_classroom.api import API
from transparent_classroom import entry_points

api = API(
    entry_points=[
        entry_points.AUTH_ENTRY_POINT,
        entry_points.LIST_ACTIVITIES_ENTRY_POINT,
        entry_points.LIST_CHILDREN_ENTRY_POINT,
        entry_points.GET_CHILD_ENTRY_POINT,
        entry_points.UPDATE_CHILD_ENTRY_POINT,
        entry_points.LIST_CLASSROOMS_ENTRY_POINT,
        entry_points.LIST_CONFERENCE_REPORTS_ENTRY_POINT,
        entry_points.LIST_EVENTS_ENTRY_POINT,
        entry_points.LIST_FORMS_ENTRY_POINT,
        entry_points.GET_FORM_ENTRY_POINT,
        entry_points.LIST_FORM_TEMPLATES_ENTRY_POINT,
        entry_points.GET_LESSON_SET_ENTRY_POINT,
        entry_points.LIST_LEVELS_ENTRY_POINT,
        entry_points.LIST_FILTERED_LEVELS_ENTRY_POINT,
        entry_points.LIST_ONLINE_APPLICATIONS_ENTRY_POINT,
        entry_points.GET_ONLINE_APPLICATION_ENTRY_POINT,
        entry_points.SUBMIT_ONLINE_APPLICATION_ENTRY_POINT,
        entry_points.ACCEPT_ONLINE_APPLICATION_ENTRY_POINT,
        entry_points.LIST_SCHOOLS_ENTRY_POINT,
        entry_points.LIST_SESSIONS_ENTRY_POINT,
        entry_points.LIST_USERS_ENTRY_POINT,
        entry_points.GET_USER_ENTRY_POINT
    ]
)
