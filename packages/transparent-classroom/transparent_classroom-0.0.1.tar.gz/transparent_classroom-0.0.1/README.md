# Transparent Classroom Client (Unofficial)
The Transparent Classroom Python client is a light-weight client for accessing Transparent Classroom's data programmatically. 
[Transparent Classroom](https://www.transparentclassroom.com/) is a student record tracking and observation tool widely 
used by Montessori schools and educators. This project is independent of the tools developed by the main Transparent 
Classroom team. For this reason, the developers of this project refer to it as the ("unofficial") client for the [Transparent
Classroom API](https://www.transparentclassroom.com/api). There is no officially supported Python client, and this "unofficial"
version adapts only the **read operations** available on the API.

The goal of this project is to help educators and technical staff automate reporting or develop utilities around the main
Transparent Classroom ecosystem. The standards, observations, and intentionality cultivated in Montessori schools provides
a wealth of data; it is often difficult, however, to leverage. Making this information more accessible to educators is meant
to improve decision-making about the well-being and care for children. 

The [Transparent Classroom API](https://www.transparentclassroom.com/api) has limitations with respect to the retrievable
objects and the fields retrieved in calls made to specific objects. For example, listing users will return User objects 
that do not contain address and/or certain pieces of contact information, while retrieving a single user will return all
of this data. These limitations just need to be noted and understood when developing code around the API.

## Setting up the Client
```
from transparent_classroom.clients import Client

# Optionally, you can specify the school (school_id) or masquerade as another user (masquerade_id).
client = Client(email='email', password='password')
```

## Requesting Data
```
client.get_schools()[0].to_dict()

{
    'id': 12345678, 
    'name': 'School Name 1', 
    'phone': '987-654-3210', 
    'address': '123 Example St, WI 54321 US', 
    'type': 'School', 
    'timezone': 'America/Chicago'
}
```

## Client Accessors/Methods
The following objects are accessible via the client: 

1. Activity
   - Method(s): 
     - get_activities(...) -> List[`Activity`]
       - Parameter(s):
         - child_id: Optional[`int`] = None
         - classroom_id: Optional[`int`] = None
         - only_photos: Optional[`bool`] = False
         - only_portfolio: Optional[`bool`] = False
         - after: Optional[Union[`str`, `date`]] = None
         - before: Optional[Union[`str`, `date`]] = None
   - `Activity` Object Field(s):
     - id (`int`)
     - author_id (`int`)
     - classroom_id (`int`)
     - normalized_text (`str`)
     - html (`str`)
     - date (`date`)
     - staff_unprocessed (`bool`)
     - photo_url (`str`)
     - medium_photo_url (`str`)
     - large_photo_url (`str`)
     - original_photo_url (`str`)
     - created_at (`datetime`)
2. Child
   - Method(s):
     - get_child(...) -> `Child`
       - Parameter(s):
         - child_id: `int`
         - as_of: Optional[Union[`str`, `date`]] = None
     - get_children(...) -> List[`Child`]
       - Parameter(s):
         - classroom_id: Optional[`int`] = None
         - session_id: Optional[`int`] = None
         - only_current: Optional[`bool`] = False
   - `Child` Object Field(s): 
     - id: Optional[`int`]
     - first_name: Optional[`str`]
     - middle_name: Optional[`str`]
     - last_name: Optional[`str`]
     - birth_date: Optional[Union[`datetime.date`, `str`]]
     - gender: Optional[`str`]
     - profile_photo: Optional[`str`]
     - program: Optional[`str`]
     - ethnicity: Optional[List[`str`]]
     - household_income: Optional[`str`]
     - dominant_language: Optional[`str`]
     - grade: Optional[`str`]
     - student_id: Optional[`str`]
     - hours_string: Optional[`str`]
     - allergies: Optional[`str`]
     - notes: Optional[`str`]
     - first_day: Optional[Union[`datetime.date`, `str`]]
     - last_day: Optional[Union[`datetime.date`, `str`]]
     - exit_notes: Optional[`str`]
     - exit_reason: Optional[`str`]
     - exit_survey_id: Optional[`int`]
     - approved_adults_string: Optional[`str`]
     - emergency_contacts_string: Optional[`str`]
     - parent_ids: Optional[List[`int`]]
     - classroom_ids: Optional[List[`int`]]
3. Classroom
   - Method(s): 
     - get_classrooms(...) -> List[`Classroom`]
       - Parameter(s):
         - show_inactive: Optional`[bool`] = False
   - `Classroom` Object Field(s): 
     - id: Optional[`int`]
     - name: Optional[`str`]
     - lesson_set_id: Optional[`int`]
     - level: Optional[`str`]
     - active: Optional[`bool`]
4. Conference Report
   - Method(s): 
     - get_conference_reports(...) -> List[`ConferenceReport`]
       - Parameter(s):
         - child_id: Optional[`int`] = None,
         - after: Optional[Union[`str`, `date`]] = None,
         - before: Optional[Union[`str`, `date`]] = None
   - `ConferenceReport` Object Field(s): 
     - id: Optional[`int`]
     - name: Optional[`str`]
     - child_id: Optional[`int`]
     - widgets: Optional[List[`Widget`]]
5. Event
   - Method(s): 
     - get_events(...) -> List[`Event`]
       - Parameter(s):
         - child_id: `int`
         - start_date: Union[`str`, `date`]
         - end_date: Union[`str`, `date`]
   - `Event` Object Field(s):
     - id: Optional[`int`]
     - classroom_id: Optional[`int`]
     - child_id: Optional[`int`]
     - event_type: Optional[`str`]
     - value: Optional[`str`]
     - created_by_id: Optional[`int`]
     - value2: Optional[`str`]
     - created_by_name: Optional[`str`]
     - time: Optional[Union[`datetime.datetime`, `str`]]
6. Form
   - Method(s): 
     - get_form(...) -> `Form`
       - Parameter(s):
         - form_id: `int`
     - get_forms(...) -> List[`Form`]
       - Parameter(s):
         - form_template_id: Optional[`int`] = None,
         - child_id: Optional[`int`] = None,
         - after: Optional[Union[`str`, `date`]] = None,
         - before: Optional[Union[`str`, `date`]] = None
   - `Form` Object Field(s): 
     - id: Optional[`int`]
     - form_template_id: Optional[`int`]
     - state: Optional[`str`]
     - child_id: Optional[`int`]
     - fields: Optional[List[`Widget`]]
     - created_at: Optional[Union[`datetime.datetime`, `str`]]
7. Form Template
   - Method(s): 
     - get_form_templates(...) -> List[`FormTemplate`]
       - Parameter(s):
   - `FormTemplate` Object Field(s): 
     - id: Optional[`int`]
     - name: Optional[`str`]
     - widgets: Optional[List[`Widget`]]
8. Lesson Set 
   - Method(s): 
     - get_lesson_set(...) -> `LessonSet`
       - Parameter(s):
         - lesson_set_id: `int`
         - format: Optional[`str`] = "short"
   - `LessonSet` Object Field(s): 
     - id: Optional[`int`]
     - name: Optional[`str`]
     - type: Optional[`str`]
     - areas: Optional[List[`Area`]]
     - scales: Optional[List[`Scale`]]
9. Level
   - Method(s): 
     - get_levels(...) -> List[`Level`]
       - Parameter(s):
         - child_id: `int`
         - lesson_set_id: Optional[`int`] = None
     - get_levels_in_date_range(...) -> List[`Level`]
       - Parameter(s):
         - child_id: `int`
         - start_date: Union[`str`, `date`]
         - end_date: Union[`str`, `date`]
   - `Level` Object Field(s): 
     - child_id: Optional[`int`]
     - lesson_id: Optional[`int`]
     - proficiency: Optional[`int`]
     - date: Optional[Union[`datetime.date`, `str`]]
     - planned: Optional[`bool`]
10. Online Application
    - Method(s):
      - get_online_application(...) -> `OnlineApplication`
        - Parameter(s):
          - online_application_id: `int`
      - get_online_applications(...) -> List[`OnlineApplication`]
        - Parameter(s):
          - after: Optional[Union[str, date, datetime]] = None
    - `OnlineApplication` Object Field(s): 
      - id: Optional[`int`]
      - school_id: Optional[`int`]
      - type: Optional[`str`]
      - state: Optional[`str`]
      - fields: Optional[List[`Widget`]]
11. School
    - Method(s):
      - get_schools(...) -> List[`School`]
        - Parameter(s):
    - `School` Object Field(s): 
      - id: Optional[`int`]
      - name: Optional[`str`]
      - phone: Optional[`str`]
      - address: Optional[`str`]
      - type: Optional[`str`]
      - timezone: Optional[`str`]
12. Session
    - Method(s):
      - get_sessions(...) -> List[`Session`]
        - Parameter(s):
      - `Session` Object Field(s): 
        - id: Optional[`int`]
        - name: Optional[`str`]
        - start_date: Optional[Union[`datetime.date`, `str`]]
        - stop_date: Optional[Union[`datetime.date`, `str`]]
        - children: Optional[`int`]
        - current: Optional[`bool`]
        - inactive: Optional[`bool`]
13. User
    - Method(s):
      - get_user(...) -> `User`
        - Parameter(s):
          - user_id: `int`
    - get_users(...) -> List[`User`]
      - Parameter(s):
        - classroom_id: Optional[`int`] = None
        - roles: Optional[List[`str`]] = None
    - `User` Object Field(s):
      - id: Optional[int] = None,
      - type: Optional[str]
      - inactive: Optional[bool]
      - email: Optional[str]
      - first_name: Optional[str]
      - last_name: Optional[str]
      - roles: Optional[List[str]]
      - accessible_classroom_ids: Optional[List[int]]
      - default_classroom_id: Optional[int]
      - street: Optional[str]
      - postal_code: Optional[str]
      - city: Optional[str]
      - state_province: Optional[str]
      - home_number: Optional[str]
      - mobile_number: Optional[str]
      - work_number: Optional[str]
