from transparent_classroom.api.enums import HTTPMethod
from transparent_classroom.api.interfaces import fields
from transparent_classroom.api.interfaces import Interface
from transparent_classroom.api.enums import EndpointBehavior


# Headers used for authentication and scoping
_AUTH_HEADERS = [
    fields.InterfaceField(base=fields.StringField(name="X-TransparentClassroomToken", is_required=True)),
    fields.InterfaceField(base=fields.StringField(name="X-TransparentClassroomMasqueradeId")),
    fields.InterfaceField(base=fields.StringField(name="X-TransparentClassroomSchoolId"))
]

# Parameters for pagination and page list limits
_PAGING_PARAMETERS = [
    fields.InterfaceField(base=fields.PositiveIntegerField(name="page")),
    fields.InterfaceField(base=fields.PositiveIntegerField(name="per_page"))
]

# Interface(s) for authenticating with the Transparent Classroom auth service
AUTH_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW,
    parameters=[
        fields.InterfaceField(base=fields.StringField(name="email", is_required=True)),
        fields.InterfaceField(base=fields.StringField(name="password", is_required=True))
    ]
)

# Interface(s) for interacting with the activity objects.
LIST_ACTIVITIES_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="child_id")),
        fields.InterfaceField(base=fields.ModelIdField(name="classroom_id")),
        fields.InterfaceField(base=fields.BooleanField(name="only_photos")),
        fields.InterfaceField(base=fields.BooleanField(name="only_portfolio")),
        fields.InterfaceField(fields.DateField(name="date_start")),
        fields.InterfaceField(fields.DateField(name="date_end"))
    ] + _PAGING_PARAMETERS
)

# Interface(s) for interacting with children objects.
LIST_CHILDREN_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="classroom_id")),
        fields.InterfaceField(base=fields.ModelIdField(name="session_id")),
        fields.InterfaceField(base=fields.BooleanField(name="only_current"))
    ]
)
GET_CHILD_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.DateField(name="as_of"))
    ]
)
"""
TODO:
    - Finish field definitions
    
"""
UPDATE_CHILD_INTERFACE = Interface(
    method=HTTPMethod.PUT,
    behavior=EndpointBehavior.UPDATE,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.StringField(name="first_name")),
        fields.InterfaceField(base=fields.StringField(name="last_name")),
        fields.InterfaceField(base=fields.DateField(name="birth_date")),
        fields.InterfaceField(base=fields.Field(name="gender")),
        fields.InterfaceField(base=fields.StringField(name="program")),
        fields.InterfaceField(base=fields.Field(name="ethnicity")),
        fields.InterfaceField(base=fields.Field(name="household_income")),
        fields.InterfaceField(base=fields.Field(name="dominant_language")),
        fields.InterfaceField(base=fields.Field(name="grade")),
        fields.InterfaceField(base=fields.StringField(name="student_id")),
        fields.InterfaceField(base=fields.Field(name="hours_string")),
        fields.InterfaceField(base=fields.StringField(name="allergies")),
        fields.InterfaceField(base=fields.Field(name="approved_adults_string")),
        fields.InterfaceField(base=fields.Field(name="emergency_contacts_string")),
        fields.InterfaceField(base=fields.StringField(name="notes"))
    ]
)

# Interface(s) for interacting with classroom objects.
LIST_CLASSROOMS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.BooleanField(name="show_inactive"))
    ]
)

# Interface(s) for interacting with conference report objects.
LIST_CONFERENCE_REPORTS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="child_id")),
        fields.InterfaceField(base=fields.DateField(name="created_after")),
        fields.InterfaceField(base=fields.DateField(name="created_before"))
    ] + _PAGING_PARAMETERS
)

# Interface(s) for interacting with event objects.
LIST_EVENTS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="child_id", is_required=True)),
        fields.InterfaceField(base=fields.DateField(name="date_start", is_required=True)),
        fields.InterfaceField(base=fields.DateField(name="date_end", is_required=True))
    ] + _PAGING_PARAMETERS
)

# Interface(s) for for interacting with form objects.
LIST_FORMS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="form_template_id")),
        fields.InterfaceField(base=fields.ModelIdField(name="child_id")),
        fields.InterfaceField(base=fields.DateField(name="created_before")),
        fields.InterfaceField(base=fields.DateField(name="created_after"))
    ]
)
GET_FORM_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW,
    headers=_AUTH_HEADERS,
    parameters=[

    ]
)

# Interface(s) for for interacting with form tempalte objects.
LIST_FORM_TEMPLATES_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[

    ]
)

# Interface(s) for for interacting with lesson set objects.
GET_LESSON_SET_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.SelectField(name="format", options=["short", "long"]))
    ]
)

# Interface(s) for for interacting with level objects.
LIST_LEVELS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW_ALL,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="child_id", is_required=True)),
        fields.InterfaceField(base=fields.ModelIdField(name="lesson_set_id"))
    ] + _PAGING_PARAMETERS
)
LIST_FILTERED_LEVELS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW_FILTERED,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="child_id", is_required=True)),
        fields.InterfaceField(base=fields.DateField(name="date_start", is_required=True)),
        fields.InterfaceField(base=fields.DateField(name="date_end", is_required=True))
    ] + _PAGING_PARAMETERS
)

# Interface(s) for for interacting with online application objects.
LIST_ONLINE_APPLICATIONS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.DateTimeField(name="created_at"))
    ]
)
GET_ONLINE_APPLICATION_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW,
    headers=_AUTH_HEADERS,
    parameters=[

    ]
)
"""
TODO:
    - Finish field definitions
    
"""
SUBMIT_ONLINE_APPLICATION_INTERFACE = Interface(
    method=HTTPMethod.POST,
    behavior=EndpointBehavior.SUBMIT,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.Field(name="fields")),
        fields.InterfaceField(base=fields.ModelIdField(name="template_id")),
        fields.InterfaceField(base=fields.BooleanField(name="silence_notifications", is_required=True))
    ]
)
ACCEPT_ONLINE_APPLICATION_INTERFACE = Interface(
    method=HTTPMethod.POST,
    behavior=EndpointBehavior.ACCEPT,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="classroom_id", is_required=True))
    ]
)

# Interface(s) for for interacting with school objects.
LIST_SCHOOLS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[

    ]
)

# Interface(s) for for interacting with session objects.
LIST_SESSIONS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[

    ]
)

# Interface(s) for for interacting with user objects.
LIST_USERS_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.LIST,
    headers=_AUTH_HEADERS,
    parameters=[
        fields.InterfaceField(base=fields.ModelIdField(name="classroom_id")),
        fields.InterfaceField(
            base=fields.MultiSelectField(
                name="roles[]",
                options=[
                    "teacher",
                    "parent",
                    "admin",
                    "billing_manager",
                    "family_member"
                ]
            )
        )
    ]
)
GET_USER_INTERFACE = Interface(
    method=HTTPMethod.GET,
    behavior=EndpointBehavior.SHOW,
    headers=_AUTH_HEADERS,
    parameters=[

    ]
)
