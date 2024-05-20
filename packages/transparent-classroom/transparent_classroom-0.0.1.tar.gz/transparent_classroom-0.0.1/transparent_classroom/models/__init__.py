import abc
import datetime
from typing import List, Optional, Dict, Any, Union
from transparent_classroom.models.utilities import Formatter
from collections import defaultdict


class JSONModel(abc.ABC):
    """
    JSON Model Class

    Abstract class providing methods for converting objects to dict and JSON-safe strings.

    Attributes:


    """

    def to_dict(self) -> Dict:
        """
        Convert the object to a dict.

        :return: Dict

        """

        data = {}
        prefix = ''.join(['_', self.__class__.__name__, '__'])

        for key, value in vars(self).items():
            if not key.startswith(prefix):
                if isinstance(value, list):
                    tmp = []

                    for item in value:
                        if hasattr(item, 'to_dict'):
                            tmp.append(item.to_dict())
                        else:
                            tmp.append(item)

                    value = tmp

                data[key.lstrip("_")] = value

        return data

    def to_json(self) -> Dict:
        """
        Convert the object to JSON-safe dict.

        :return: Dict

        """

        return Formatter.jsonify(data=self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict) -> Any:
        """
        Convert an object from the provided data.

        :param data: Dict, The data to use for object construction.
        :return: Any

        """

        instance = cls()

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        return instance


class Model(JSONModel):
    """
    Model Abstract Base Class

    Attributes:
        id (`int`): The id of the Transparent Classroom object.

    """

    def __init__(self, id: Optional[int] = None) -> None:
        """
        Model Constructor

        :param id: Optional[int], The id of the Transparent Classroom object.
        :return: None

        """

        self.id = id
        super().__init__()

    @property
    def id(self) -> int:
        """
        The Transparent Classroom object id.

        :return: int

        """

        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        Set the id of the Transparent Classroom object.

        :param value: int, The Transparent Classroom object id.
        :return: None

        """

        self._id = value


class Activity(Model):
    """
    Activity Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the activity.
        author_id (`int`): The id of the author who created the activity record.
        classroom_id (`int`): The id of the classroom where the activity occurred.
        normalized_text (`str`): The text describing the activity.
        html (`str`): The HTML-string associated with the activity.
        date (`date`): The date the activity occurred upon.
        staff_unprocessed (`bool`): Flag indicating whether the activity has been
            processed by a school staff member.
        photo_url (`str`): The url to the photo of the activity.
        medium_photo_url (`str`): The (medium/resized) url to the photo of the activity.
        large_photo_url (`str`): The (large/resized) url to the photo of the activity.
        original_photo_url (`str`): The url to the original photo of the activity.
        created_at (`datetime`): The datetime/timestamp that the activity was recorded.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            author_id: Optional[int] = None,
            classroom_id: Optional[int] = None,
            normalized_text: Optional[str] = None,
            html: Optional[str] = None,
            date: Optional[Union[datetime.date, str]] = None,
            staff_unprocessed: Optional[bool] = None,
            photo_url: Optional[str] = None,
            medium_photo_url: Optional[str] = None,
            large_photo_url: Optional[str] = None,
            original_photo_url: Optional[str] = None,
            created_at: Optional[Union[datetime.datetime, str]] = None) -> None:
        """

        :param id: Optional[int], The Transparent Classroom object id of the activity.
        :param author_id: Optional[int], The id of the author who created the activity record.
        :param classroom_id: Optional[int], The id of the classroom where the activity occurred.
        :param normalized_text: Optional[str], The text describing the activity.
        :param html: Optional[str], The HTML-string associated with the activity.
        :param date: Optional[Union[date, str]], The date the activity occurred upon.
        :param staff_unprocessed: Optional[bool], Flag indicating whether the activity has been
            processed by a school staff member.
        :param photo_url: Optional[str], The url to the photo of the activity.
        :param medium_photo_url: Optional[str], The (medium/resized) url to the photo of the activity.
        :param large_photo_url: Optional[str], The (large/resized) url to the photo of the activity.
        :param original_photo_url: Optional[str], The url to the original photo of the activity.
        :param created_at: Optional[Union[datetime, str]], The datetime/timestamp that the
            activity was recorded.
        :return: None

        """

        super().__init__(id=id)
        self.author_id = author_id
        self.classroom_id = classroom_id
        self.normalized_text = normalized_text
        self.html = html
        self.date = date
        self.staff_unprocessed = staff_unprocessed
        self.photo_url = photo_url
        self.medium_photo_url = medium_photo_url
        self.large_photo_url = large_photo_url
        self.original_photo_url = original_photo_url
        self.created_at = created_at

    @property
    def author_id(self) -> int:
        """
        The id of the author who created the activity record.

        :return: int

        """

        return self._author_id

    @author_id.setter
    def author_id(self, value: int) -> None:
        """
        Set the id of the author who created the record.

        :param value: int, The id of the author who created the activity record.
        :return: None

        """

        self._author_id = value

    @property
    def classroom_id(self) -> int:
        """
        The id of the classroom whether the activity originated.

        :return: int

        """

        return self._classroom_id

    @classroom_id.setter
    def classroom_id(self, value: int) -> None:
        """
        Set the id of the classroom whether the activity originated.

        :param value: int, The id of the classroom whether the activity originated.
        :return: None

        """

        self._classroom_id = value

    @property
    def normalized_text(self) -> str:
        """
        The text describing the activity.

        :return: str

        """

        return self._normalized_text

    @normalized_text.setter
    def normalized_text(self, value: str) -> None:
        """
        Set the text describing the activity.

        :param value: str, The text describing the activity.
        :return: None

        """

        self._normalized_text = value

    @property
    def html(self) -> str:
        """
        The HTML-string associated with the activity.

        :return: str

        """

        return self._html

    @html.setter
    def html(self, value: str) -> None:
        """
        Set the HTML-string of the activity.

        :param value: str, The HTML to associate with the activity.
        :return: None

        """

        self._html = value

    @property
    def date(self) -> datetime.date:
        """
        The date the activity occurred upon.

        :return: date

        """

        return self._date

    @date.setter
    def date(self, value: Union[datetime.date, str]) -> None:
        """
        Set the date the activity occurred upon.

        :param value: Union[date, str], The date the activity occurred upon.
        :return: None

        """

        self._date = Formatter.str_to_date(value=value)

    @property
    def staff_unprocessed(self) -> bool:
        """
        The flag indicating whether the activity has been processed by a school staff member.

        :return: bool

        """

        return self._staff_unprocessed

    @staff_unprocessed.setter
    def staff_unprocessed(self, value: bool) -> None:
        """
        Set the flag indicating whether the activity has been processed by a school staff member.

        :param value: bool, The flag indicating whether the activity has been processed by a
            school staff member.
        :return: None

        """

        self._staff_unprocessed = value

    @property
    def photo_url(self) -> str:
        """
        The url to the photo of the activity.

        :return: str

        """

        return self._photo_url

    @photo_url.setter
    def photo_url(self, value: str) -> None:
        """
        Set the url to the photo of the activity.

        :param value: str, The url to the photo of the activity.
        :return: None

        """

        self._photo_url = value

    @property
    def medium_photo_url(self) -> str:
        """
        The (medium/resized) url to the photo of the activity.

        :return: str

        """

        return self._medium_photo_url

    @medium_photo_url.setter
    def medium_photo_url(self, value: str) -> None:
        """
        Set the (medium/resized) url to the photo of the activity.

        :param value: str, The (medium/resized) url to the photo of the activity.
        :return: None

        """

        self._medium_photo_url = value

    @property
    def large_photo_url(self) -> str:
        """
        The (large/resized) url to the photo of the activity.

        :return: str

        """

        return self._large_photo_url

    @large_photo_url.setter
    def large_photo_url(self, value: str) -> None:
        """
        Set the (large/resized) url to the photo of the activity.

        :param value: str, The (large/resized) url to the photo of the activity.
        :return: None

        """

        self._large_photo_url = value

    @property
    def original_photo_url(self) -> str:
        """
        The url to the original photo of the activity.

        :return: str

        """

        return self._original_photo_url

    @original_photo_url.setter
    def original_photo_url(self, value: str) -> None:
        """
        Set the url to the original photo of the activity.

        :param value: str, The url to the original photo of the activity.
        :return: None

        """

        self._original_photo_url = value

    @property
    def created_at(self) -> datetime:
        """
        The datetime/timestamp that the activity was recorded.

        :return: datetime

        """

        return self._created_at

    @created_at.setter
    def created_at(self, value: Union[datetime.datetime, str]) -> None:
        """
        Set the datetime/timestamp that the activity was recorded.

        :param value: Union[datetime, str], The datetime/timestamp that the activity was recorded.
        :return: None

        """

        self._created_at = Formatter.str_to_datetime(value=value)


class Child(Model):
    """
    Child Model Class

    Attributes:
        id (`int`): The id of the child in Transparent Classroom.
        first_name (`str`): The child's first name.
        middle_name (`str`): The child's middle name.
        last_name (`str`): The child's last name.
        birth_date (`date`): The child's date of birth.
        gender (`str`): The child's gender.
        profile_photo (`str`): URL to the child's profile picture.
        program (`str`): The school program that the child belongs to.
        ethnicity (`List[str]`): A list of the child's ethnicity identities
        household_income (`str`): A text description of the child's household
            income.
        dominant_language (`str`): The child's dominant language.
        grade (`str`): The grade-level of the student (3rd, 4th, etc.)
        student_id (`str`): The id of the student.
        hours_string (`str`): The hours/days string detailing when the
            child attends the school/program.
        allergies (`str`): A description of the child's allergies, if any.
        notes (`str`): Notes about the child.
        first_day (`date`): The date of the child's first day at
            the associated school/program.
        last_day (`date`): The date of the child's last day (if
            applicable) that the student attended the school/program.
        exit_notes (`str`): Notes provided by staff/families taken when the
            child/family (if applicable) was leaving the school.
        exit_reason (`str`): The reason (if the student has left the school)
            of why the child/family left the school.
        exit_survey_id (`int`): The id of the exit survey (if the student
            has left the school) form.
        approved_adults_string (`str`): The adults approved as guardians for the
            child (picking them up, etc.).
        emergency_contacts_string (`str`): The contact details to use in the case
            of an emergency.
        parent_ids (`List[int]`): List of the child's parent/guardian ids.
        classroom_ids (`List[int]`): List of the classroom  ids that the
            child belongs to at the school.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            first_name: Optional[str] = None,
            middle_name: Optional[str] = None,
            last_name: Optional[str] = None,
            birth_date: Optional[Union[datetime.date, str]] = None,
            gender: Optional[str] = None,
            profile_photo: Optional[str] = None,
            program: Optional[str] = None,
            ethnicity: Optional[List[str]] = None,
            household_income: Optional[str] = None,
            dominant_language: Optional[str] = None,
            grade: Optional[str] = None,
            student_id: Optional[str] = None,
            hours_string: Optional[str] = None,
            allergies: Optional[str] = None,
            notes: Optional[str] = None,
            first_day: Optional[Union[datetime.date, str]] = None,
            last_day: Optional[Union[datetime.date, str]] = None,
            exit_notes: Optional[str] = None,
            exit_reason: Optional[str] = None,
            exit_survey_id: Optional[int] = None,
            approved_adults_string: Optional[str] = None,
            emergency_contacts_string: Optional[str] = None,
            parent_ids: Optional[List[int]] = None,
            classroom_ids: Optional[List[int]] = None) -> None:
        """
        Child Object Constructor

        :param id: Optional[int], The id of the child in Transparent Classroom.
        :param first_name: Optional[str], The child's first name.
        :param middle_name: Optional[str], The child's middle name.
        :param last_name: Optional[str], The child's last name.
        :param birth_date: Optional[Union[date, str]], The child's date of birth.
        :param gender: Optional[str], The child's gender.
        :param profile_photo: Optional[str], URL to the child's profile picture.
        :param program: Optional[str], The school program that the child belongs to.
        :param ethnicity: Optional[List[str]], A list of the child's ethnicity identities.
        :param household_income: Optional[str], A text description of the child's
            household income.
        :param dominant_language: Optional[str], The child's dominant language.
        :param grade: Optional[str], The grade-level of the student (3rd, 4th, etc.)
        :param student_id: Optional[str], The id of the student.
        :param hours_string: Optional[str], The hours/days string detailing when the
            child attends the school/program.
        :param allergies: Optional[str], A description of the child's allergies, if any.
        :param notes: Optional[str], Notes about the child.
        :param first_day: Optional[Union[date, str]], The date of the child's first day at
            the associated school/program.
        :param last_day: Optional[Union[date, str]], The date of the child's last day (if
            applicable) that the student attended the school/program.
        :param exit_notes: Optional[str], Notes provided by staff/families taken when the
            child/family (if applicable) was leaving the school.
        :param exit_reason: Optional[str], The reason (if the student has left the school)
            of why the child/family left the school.
        :param exit_survey_id: Optional[int], The id of the exit survey (if the student
            has left the school) form.
        :param approved_adults_string: Optional[str], The adults approved as guardians for
            the child (picking them up, etc.).
        :param emergency_contacts_string: Optional[str], The contact details to use in the
            case of an emergency.
        :param parent_ids: Optional[List[int]], List of the child's parent/guardian ids.
        :param classroom_ids: Optional[List[int]], List of the classroom ids that the
            child belongs to at the school.
        :return: None

        """

        super().__init__(id=id)
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.profile_photo = profile_photo
        self.program = program
        self.ethnicity = ethnicity
        self.household_income = household_income
        self.dominant_language = dominant_language
        self.grade = grade
        self.student_id = student_id
        self.hours_string = hours_string
        self.allergies = allergies
        self.notes = notes
        self.first_day = first_day
        self.last_day = last_day
        self.exit_notes = exit_notes
        self.exit_reason = exit_reason
        self.exit_survey_id = exit_survey_id
        self.approved_adults_string = approved_adults_string
        self.emergency_contacts_string = emergency_contacts_string
        self.parent_ids = parent_ids
        self.classroom_ids = classroom_ids

    @property
    def first_name(self) -> str:
        """
        The first name of the child in Transparent Classroom.

        :return: str

        """

        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Set the first name of the child object.

        :param value: str, The first name of the child.
        :return: None

        """

        self._first_name = value

    @property
    def middle_name(self) -> str:
        """
        The middle name of the child in Transparent Classroom.

        :return: str

        """

        return self._middle_name

    @middle_name.setter
    def middle_name(self, value: str) -> None:
        """
        Set the middle name of the child object.

        :param value: str, The middle name of the child.
        :return: None

        """

        self._middle_name = value

    @property
    def last_name(self) -> str:
        """
        The last name of the child in Transparent Classroom.

        :return: str

        """

        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Set the last name of the child object.

        :param value: str, The last name of the child.
        :return: None

        """

        self._last_name = value

    @property
    def birth_date(self) -> datetime.date:
        """
        The child's date of birth.

        :return: date

        """

        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: Union[datetime.date, str]) -> None:
        """
        Set the child's date of birth.

        :param value: Union[date, str], The date of birth of the child.
        :return: None

        """

        self._birth_date = Formatter.str_to_date(value=value)

    @property
    def gender(self) -> str:
        """
        The gender of the child in Transparent Classroom.

        :return: str

        """

        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        """
        Set the gender of the child object.

        :param value: str, The gender of the child.
        :return: None

        """

        self._gender = value

    @property
    def profile_photo(self) -> str:
        """
        The url to the child's Transparent Classroom profile photo.

        :return: str

        """

        return self._profile_photo

    @profile_photo.setter
    def profile_photo(self, value: str) -> None:
        """
        Set the url of the child's profile photo.

        :param value: str, The gender of the child.
        :return: None

        """

        self._profile_photo = value

    @property
    def program(self) -> str:
        """
        The school program that the child belongs to.

        :return: str

        """

        return self._program

    @program.setter
    def program(self, value: str) -> None:
        """
        Set the school program that the child belongs to.

        :param value: str, The school program that the child belongs to.
        :return: None

        """

        self._program = value

    @property
    def ethnicity(self) -> List[str]:
        """
        A list of the child's ethnicity identities.

        :return: List[str]

        """

        return self._ethnicity

    @ethnicity.setter
    def ethnicity(self, value: List[str]) -> None:
        """
        Set the list of the child's ethnicity identities.

        :param value: List[str], The list of the child's ethnicity identities.
        :return: None

        """

        self._ethnicity = value

    @property
    def household_income(self) -> str:
        """
        The text description of the child's household income.

        :return: str

        """

        return self._household_income

    @household_income.setter
    def household_income(self, value: str) -> None:
        """
        Set the text description of the child's household income.

        :param value: str, The text description of the child's household income.
        :return: None

        """

        self._household_income = value

    @property
    def dominant_language(self) -> str:
        """
        The child's dominant language.

        :return: str

        """

        return self._dominant_language

    @dominant_language.setter
    def dominant_language(self, value: str) -> None:
        """
        Set the child's dominant language.

        :param value: str, The child's dominant language.
        :return: None

        """

        self._dominant_language = value

    @property
    def grade(self) -> str:
        """
        The grade-level of the student (3rd, 4th, etc.)

        :return: str

        """

        return self._grade

    @grade.setter
    def grade(self, value: str) -> None:
        """
        Set the grade-level of the student (3rd, 4th, etc.)

        :param value: str, The grade-level of the student (3rd, 4th, etc.)
        :return: None

        """

        self._grade = value

    @property
    def student_id(self) -> str:
        """
        The id of the student.

        :return: str

        """

        return self._student_id

    @student_id.setter
    def student_id(self, value: str) -> None:
        """
        Set the id of the student.

        :param value: str, The id of the student.
        :return: None

        """

        self._student_id = value

    @property
    def hours_string(self) -> str:
        """
        The hours/days string detailing when the child attends the school/program.

        :return: str

        """

        return self._hours_string

    @hours_string.setter
    def hours_string(self, value: str) -> None:
        """
        Set the hours/days string detailing when the child attends the school/program.

        :param value: str, The hours/days string detailing when the child attends the school/program.
        :return: None

        """

        self._hours_string = value

    @property
    def allergies(self) -> str:
        """
        The description of the child's allergies, if any.

        :return: str

        """

        return self._allergies

    @allergies.setter
    def allergies(self, value: str) -> None:
        """
        Set the description of the child's allergies, if any.

        :param value: str, The description of the child's allergies, if any.
        :return: None

        """

        self._allergies = value

    @property
    def notes(self) -> str:
        """
        The notes about the child.

        :return: str

        """

        return self._notes

    @notes.setter
    def notes(self, value: str) -> None:
        """
        Set the notes about the child.

        :param value: str, The notes about the child.
        :return: None

        """

        self._notes = value

    @property
    def first_day(self) -> datetime.date:
        """
        The date of the child's first day at the associated school/program.

        :return: date

        """

        return self._first_day

    @first_day.setter
    def first_day(self, value: Union[datetime.date, str]) -> None:
        """
        Set the date of the child's first day at the associated school/program.

        :param value: Union[date, str], The date of the child's first day at the associated school/program.
        :return: None

        """

        self._first_day = Formatter.str_to_date(value=value)

    @property
    def last_day(self) -> datetime.date:
        """
        The date of the child's last day (if applicable) that the student attended the school/program.

        :return: date

        """

        return self._last_day

    @last_day.setter
    def last_day(self, value: Union[datetime.date, str]) -> None:
        """
        Set the date of the child's last day (if applicable) that the student attended the school/program.

        :param value: Union[date, str], The date of the child's last day (if applicable) that the student attended
            the school/program.
        :return: None

        """

        self._last_day = Formatter.str_to_date(value=value)

    @property
    def exit_notes(self) -> str:
        """
        Notes provided by staff/families taken when the child/family (if applicable) was leaving the school.

        :return: str

        """

        return self._exit_notes

    @exit_notes.setter
    def exit_notes(self, value: str) -> None:
        """
        Set the notes provided by staff/families taken when the child/family (if applicable) was leaving the school.

        :param value: str, The notes provided by staff/families taken when the child/family (if applicable) was
            leaving the school.
        :return: None

        """

        self._exit_notes = value

    @property
    def exit_survey_id(self) -> int:
        """
        The id of the exit survey (if the student has left the school) form.

        :return: int

        """

        return self._exit_survey_id

    @exit_survey_id.setter
    def exit_survey_id(self, value: int) -> None:
        """
        Set the id of the exit survey (if the student has left the school) form.

        :param value: int, The id of the exit survey (if the student has left the school) form.
        :return: None

        """

        self._exit_survey_id = value

    @property
    def approved_adults_string(self) -> str:
        """
        The adults approved as guardians for the child (picking them up, etc.).

        :return: str

        """

        return self._approved_adults_string

    @approved_adults_string.setter
    def approved_adults_string(self, value: str) -> None:
        """
        Set the adults approved as guardians for the child (picking them up, etc.).

        :param value: str, The adults approved as guardians for the child (picking
            them up, etc.).
        :return: None

        """

        self._approved_adults_string = value

    @property
    def emergency_contacts_string(self) -> str:
        """
        The contact details to use in the case of an emergency.

        :return: str

        """

        return self._emergency_contacts_string

    @emergency_contacts_string.setter
    def emergency_contacts_string(self, value: str) -> None:
        """
        Set the contact details to use in the case of an emergency.

        :param value: str, The contact details to use in the case of an emergency.
        :return: None

        """

        self._emergency_contacts_string = value

    @property
    def parent_ids(self) -> List[int]:
        """
        The list of the child's parent/guardian ids.

        :return: List[int]

        """

        return self._parent_ids

    @parent_ids.setter
    def parent_ids(self, value: List[int]) -> None:
        """
        Set the list of the child's parent/guardian ids.

        :param value: List[int], The list of the child's parent/guardian ids.
        :return: None

        """

        self._parent_ids = value

    @property
    def classroom_ids(self) -> List[int]:
        """
        The list of the classroom ids that the child belongs to at the school.

        :return: List[int]

        """

        return self._classroom_ids

    @classroom_ids.setter
    def classroom_ids(self, value: List[int]) -> None:
        """
        Set the list of the classroom ids that the child belongs to at the school.

        :param value: List[int], The list of the classroom ids that the child belongs to at the school.
        :return: None

        """

        self._classroom_ids = value


class Classroom(Model):
    """
    Classroom Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the classroom.
        name (`str`): The name of the classroom.
        lesson_set_id (`int`): The id of the lesson set used by the classroom.
        level (`str`): The grade levels in the classroom.
        active (`bool`): Flag indicating whether the classroom is active (or actively
            in use by the school).

    """

    def __init__(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            lesson_set_id: Optional[int] = None,
            level: Optional[str] = None,
            active: Optional[bool] = None) -> None:
        """
        Classroom Constructor

        :param id: Optional[int], The Transparent Classroom object id of the classroom.
        :param name: Optional[str], The name of the classroom.
        :param lesson_set_id: Optional[int], The id of the lesson set used by the classroom.
        :param level: Optional[int], The grade levels in the classroom.
        :param active: Optional[bool], Flag indicating whether the classroom is active (or
            actively in use by the school).
        :return: None

        """

        super().__init__(id=id)
        self.name = name
        self.lesson_set_id = lesson_set_id
        self.level = level
        self.active = active

    @property
    def name(self) -> str:
        """
        The name of the classroom.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the classroom.

        :param value: str, The name of the classroom.
        :return: None

        """

        self._name = value

    @property
    def lesson_set_id(self) -> int:
        """
        The id of the lesson set used by the classroom.

        :return: int

        """

        return self._lesson_set_id

    @lesson_set_id.setter
    def lesson_set_id(self, value: int) -> None:
        """
        Set the id of the lesson set used by the classroom.

        :param value: int, The id of the lesson set used by the classroom.
        :return: None

        """

        self._lesson_set_id = value

    @property
    def level(self) -> str:
        """
        The grade levels in the classroom.

        :return: str

        """

        return self._level

    @level.setter
    def level(self, value: str) -> None:
        """
        Set the grade levels in the classroom.

        :param value: str, The grade levels in the classroom.
        :return: None

        """

        self._level = value

    @property
    def active(self) -> bool:
        """
        Flag indicating whether the classroom is active (or actively in use by the school).

        :return: bool

        """

        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        """
        Set the flag indicating whether the classroom is active (or actively in use by the school).

        :param value: bool, The flag indicating whether the classroom is active (or actively in use by the school).
        :return: None

        """

        self._active = value


class Widget(JSONModel):
    """
    Widget Class

    Attributes:
        type (`str`): The type of form widget.

    """

    def __init__(self, attributes: Optional[Dict] = None) -> None:
        """
        Widget Constructor

        :param attributes: Optional[Dict], The
        :return: None

        """

        super().__init__()
        attributes = {} if attributes is None else attributes
        self.__attributes = defaultdict(lambda: None, attributes)

        for k, v in self.__attributes.items():
            self.__setattr__(k, v)

    def get(self, key: str) -> Any:
        """
        Get the specified attribute value.

        :param key: str, The name of the attribute to return.
        :return: None

        """

        return self.__attributes.get(key)

    def remove(self, key: str) -> None:
        """
        Remove the specified attribute from the widget.

        :param key: str, The name of the attribute to remove.
        :return: None

        """

        if key in self.__attributes.keys():
            del self.__attributes[key]
            self.__delattr__(key)

    def set(self, key: str, value: Any) -> None:
        """
        Set the specified attribute name, value pair.

        :param key: str, The name of the attribute to set.
        :param value: Any, The value to associated with the key.
        :return: None

        """

        self.__attributes[key] = value
        self.__setattr__(key, value)

    def clear(self) -> None:
        """
        Remove all existing attributes defining the Widget.

        :return: None

        """

        for k in list(self.__attributes.keys()):
            self.remove(key=k)

    def reset(self, attributes: Optional[Dict] = None) -> None:
        """
        Reset the widget with the provided attributes and data.

        :param attributes: Optional[Dict], The attributes to reset the Widget with.
        :return: None

        """

        self.clear()
        attributes = {} if attributes is None else attributes
        self.__attributes = defaultdict(lambda: None, attributes)

        for k, v in self.__attributes.items():
            self.__setattr__(k, v)

    @property
    def attributes(self) -> List[str]:
        """
        The list of attribute names defining the Widget.

        :return: List[str]

        """

        return list(self.__attributes.keys())


class FormTemplate(Model):
    """
    Form Template Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the form template.
        name (`str`): The name of the form template.
        widgets (`List[Widget]`): The list of widgets composing the template.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            widgets: Optional[List[Widget]] = None) -> None:
        """
        Form Template Constructor

        :param id: Optional[int], The Transparent Classroom object id of the form template.
        :param name: Optional[str], The name of the form template.
        :param widgets: Optional[List[Widget]], The list of widgets composing the template.
        :return: None

        """

        super().__init__(id=id)
        self.name = name
        self.widgets = widgets

    @property
    def name(self) -> str:
        """
        The name of the form template.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the form template.

        :param value: str, The name of the form template.
        :return: None

        """

        self._name = value

    @property
    def widgets(self) -> List[Widget]:
        """
        The list of widgets composing the template.

        :return: List[Widget]

        """

        return self._widgets

    @widgets.setter
    def widgets(self, value: List[Widget]) -> None:
        """
        Set the list of widgets composing the template.

        :param value: List[Widget], The list of widgets composing the template.
        :return: None

        """

        self._widgets = [] if value is None else value


class ConferenceReport(FormTemplate):
    """
    Conference Report Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the conference report.
        name (`str`): The name of the conference report.
        child_id (`int`): The id of child that the conference report has been filed for.
        widgets (`List[Widget]`): The (populated) widget data filled out in the complete
            (or partially complete) conference report.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            child_id: Optional[int] = None,
            widgets: Optional[List[Widget]] = None) -> None:
        """
        Conference Report Constructor

        :param id: Optional[int], Transparent Classroom object id of the conference report.
        :param name: Optional[str], The name of the conference report.
        :param child_id: Optional[int], The id of child that the conference report has been filed for.
        :param widgets: Optional[List[Widget]], The (populated) widget data filled out in the complete
            (or partially complete) conference report.
        :return: None

        """

        super().__init__(id=id, name=name, widgets=widgets)
        self.child_id = child_id

    @property
    def child_id(self) -> int:
        """
        The id of child that the conference report has been filed for.

        :return: int

        """

        return self._child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        """
        Set the id of child that the conference report has been filed for.

        :param value: int, The id of child that the conference report has been filed for.
        :return: None

        """

        self._child_id = value


class Event(Model):
    """
    Event Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the event.
        classroom_id (`int`): The id of the classroom where the event took place.
        child_id (`int`): The id of the child associated with the event.
        event_type (`str`): The type/description of the event (e.g. toileting, etc.)
        value (`str`): The value/description of the event.
        created_by_id (`int`): The id of the staff member who created the event.
        value2 (`str`): The secondary descriptor of the event.
        created_by_name (`str`): The name of the staff member who created the event.
        time (`datetime`): The datetime that the event was created.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            classroom_id: Optional[int] = None,
            child_id: Optional[int] = None,
            event_type: Optional[str] = None,
            value: Optional[str] = None,
            created_by_id: Optional[int] = None,
            value2: Optional[str] = None,
            created_by_name: Optional[str] = None,
            time: Optional[Union[datetime.datetime, str]] = None) -> None:
        """
        Event Constructor

        :param id: Optional[int], The Transparent Classroom object id of the event.
        :param classroom_id: Optional[int], The id of the classroom where the event took place.
        :param child_id: Optional[int], The id of the child associated with the event.
        :param event_type: Optional[str], The type/description of the event (e.g. toileting, etc.)
        :param value: Optional[str], The value/description of the event.
        :param created_by_id: Optional[int], The id of the staff member who created the event.
        :param value2: Optional[str], The secondary descriptor of the event.
        :param created_by_name: Optional[str], The name of the staff member who created the event.
        :param time: Optional[Union[datetime, str]], The datetime that the event was created.
        :return: None

        """

        super().__init__(id=id)
        self.classroom_id = classroom_id
        self.child_id = child_id
        self.event_type = event_type
        self.value = value
        self.created_by_id = created_by_id
        self.value2 = value2
        self.created_by_name = created_by_name
        self.time = time

    @property
    def classroom_id(self) -> int:
        """
        The id of the classroom where the event took place.

        :return: int

        """

        return self._classroom_id

    @classroom_id.setter
    def classroom_id(self, value: int) -> None:
        """
        Set the id of the classroom where the event took place.

        :param value: int, The id of the classroom where the event took place.
        :return: None

        """

        self._classroom_id = value

    @property
    def child_id(self) -> int:
        """
        The id of the child associated with the event.

        :return: int

        """

        return self._child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        """
        Set the id of the child associated with the event.

        :param value: int, The id of the child associated with the event.
        :return: None

        """

        self._child_id = value

    @property
    def event_type(self) -> str:
        """
        The type/description of the event (e.g. toileting, etc.)

        :return: str

        """

        return self._event_type

    @event_type.setter
    def event_type(self, value: str) -> None:
        """
        Set the type/description of the event (e.g. toileting, etc.)

        :param value: str, The type/description of the event (e.g. toileting, etc.)
        :return: None

        """

        self._event_type = value

    @property
    def value(self) -> str:
        """
        The value/description of the event.

        :return: str

        """

        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """
        Set the value/description of the event.

        :param value: str, The value/description of the event.
        :return: None

        """

        self._value = value

    @property
    def created_by_id(self) -> int:
        """
        The id of the staff member who created the event.

        :return: int

        """

        return self._created_by_id

    @created_by_id.setter
    def created_by_id(self, value: int) -> None:
        """
        Set the id of the staff member who created the event.

        :param value: int, The id of the staff member who created the event.
        :return: None

        """

        self._created_by_id = value

    @property
    def value2(self) -> str:
        """
        The secondary descriptor of the event.

        :return: str

        """

        return self._value2

    @value2.setter
    def value2(self, value: str) -> None:
        """
        Set the secondary descriptor of the event.

        :param value: str, The secondary descriptor of the event.
        :return: None

        """

        self._value2 = value

    @property
    def created_by_name(self) -> str:
        """
        The name of the staff member who created the event.

        :return: str

        """

        return self._created_by_name

    @created_by_name.setter
    def created_by_name(self, value: str) -> None:
        """
        Set the name of the staff member who created the event.

        :param value: str, The name of the staff member who created the event.
        :return: None

        """

        self._created_by_name = value

    @property
    def time(self) -> datetime:
        """
        The datetime that the event was created.

        :return: datetime

        """

        return self._time

    @time.setter
    def time(self, value: Union[datetime.datetime, str]) -> None:
        """
        Set the datetime that the event was created.

        :param value: Union[datetime, str], The datetime that the event was created.
        :return: None

        """

        self._time = Formatter.str_to_datetime(value=value)


class Field(JSONModel):
    """
    Form Field Class

    Attributes:
        name (`str`): The name of the field.
        value (`Any`): The value (provided by the user) when filling out the form.

    """

    def __init__(self, name: Optional[str] = None, value: Optional[Any] = None) -> None:
        """
        Form Constructor

        :param name: Optional[str], The name of the field.
        :param value: Optional[Any], The value (provided by the user) when filling out the form.
        :return: None

        """

        super().__init__()
        self.name = name
        self.value = value

    @property
    def name(self) -> str:
        """
        The name of the field.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the field.

        :param value: str, The name of the field.
        :return: None

        """

        self._name = value

    @property
    def value(self) -> Any:
        """
        The value (provided by the user) when filling out the form.

        :return: Any

        """

        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """
        Set the value (provided by the user) when filling out the form.

        :param value: Any, The value (provided by the user) when filling out the form.
        :return: None

        """

        self._value = value


class Form(Model):
    """
    Form Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the form.
        form_template_id (`int`): The id of the form template that this form is derived from.
        state (`str`): The submission state of the form (e.g. `submitted`, etc.).
        child_id (`int`): The id of the child associated with the form submission.
        fields (`List[Widget]`): The question-answer responses provided by the respondent on the form.
        created_at (`datetime`): The datetime of when the form was created.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            form_template_id: Optional[int] = None,
            state: Optional[str] = None,
            child_id: Optional[int] = None,
            fields: Optional[List[Widget]] = None,
            created_at: Optional[Union[datetime.datetime, str]] = None) -> None:
        """
        Form Constructor

        :param id: Optional[int], The Transparent Classroom object id of the form.
        :param form_template_id: Optional[int], The id of the form template that this form is derived from.
        :param state: Optional[str], The submission state of the form (e.g. `submitted`, etc.).
        :param child_id: Optional[int], The id of the child associated with the form submission.
        :param fields: Optional[List[Widget]], The question-answer responses provided by the respondent on the form.
        :param created_at: Optional[Union[datetime, str]], The datetime of when the form was created.
        :return: None

        """

        super().__init__(id=id)
        self.form_template_id = form_template_id
        self.state = state
        self.child_id = child_id
        self.fields = fields
        self.created_at = created_at

    @property
    def form_template_id(self) -> int:
        """
        The id of the form template that this form is derived from.

        :return: int

        """

        return self._form_template_id

    @form_template_id.setter
    def form_template_id(self, value: int) -> None:
        """
        Set the id of the form template that this form is derived from.

        :param value: int, The id of the form template that this form is derived from.
        :return: None

        """

        self._form_template_id = value

    @property
    def state(self) -> str:
        """
        The submission state of the form (e.g. `submitted`, etc.).

        :return: str

        """

        return self._state

    @state.setter
    def state(self, value: str) -> None:
        """
        Set the submission state of the form (e.g. `submitted`, etc.).

        :param value: str, The submission state of the form (e.g. `submitted`, etc.).
        :return: None

        """

        self._state = value

    @property
    def child_id(self) -> int:
        """
        The id of the child associated with the form submission.

        :return: int

        """

        return self._child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        """
        Set the id of the child associated with the form submission.

        :param value: int, The id of the child associated with the form submission.
        :return: None

        """

        self._child_id = value

    @property
    def fields(self) -> List[Widget]:
        """
        The question-answer responses provided by the respondent on the form.

        :return: List[Widget]

        """

        return self._fields

    @fields.setter
    def fields(self, value: List[Widget]) -> None:
        """
        Set the question-answer responses provided by the respondent on the form.

        :param value: List[Widget], The question-answer responses provided by the respondent
            on the form.
        :return: None

        """

        self._fields = [] if value is None else value

    @property
    def created_at(self) -> datetime:
        """
        The datetime of when the form was created.

        :return: datetime

        """

        return self._created_at

    @created_at.setter
    def created_at(self, value: Union[datetime.datetime, str]) -> None:
        """
        Set the datetime of when the form was created.

        :param value: Union[datetime, str], The datetime of when the form was created.
        :return: None

        """

        self._created_at = Formatter.str_to_datetime(value=value)


class ArchetypeInterface(Model):
    """
    Archetype Interface Model Class

    The Archetype Interface is a set of attributes common to the nested
    objects found in a lesson set.

    Attributes:
        id (`int`): The Transparent Classroom object id of the lesson set.
        archetype_id (`int`): The id of the archetype.
        name (`str`): The name of the lesson, group, or material being worked.
        type (`str`): The type of the archetype object (group, lesson, etc.)
        description (`str`): The description of the object.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            archetype_id: Optional[int] = None,
            name: Optional[str] = None,
            type: Optional[str] = None,
            description: Optional[str] = None):
        """
        ArchetypeInterface Constructor

        :param id: Optional[int], The Transparent Classroom object id of the archetyped object.
        :param archetype_id: Optional[int], The id of the archetype.
        :param name: Optional[str], The name of the lesson, group, or material being worked.
        :param type: Optional[str], The type of the archetype object (group, lesson, etc.)
        :param description: Optional[str], The description of the object.
        :return: None

        """

        super().__init__(id=id)
        self.archetype_id = archetype_id
        self.name = name
        self.type = type
        self.description = description

    @property
    def archetype_id(self) -> int:
        """
        The id of the archetype.

        :return: int

        """

        return self._archetype_id

    @archetype_id.setter
    def archetype_id(self, value: int) -> None:
        """
        Set the id of the archetype.

        :param value: int, The id of the archetype.
        :return: None

        """

        self._archetype_id = value

    @property
    def name(self) -> str:
        """
        The name of the lesson, group, or material being worked.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the lesson, group, or material being worked.

        :param value: str, The name of the lesson, group, or material being worked.
        :return: None

        """

        self._name = value

    @property
    def type(self) -> str:
        """
        The type of the archetype object (group, lesson, etc.)

        :return: str

        """

        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """
        Set the type of the archetype object (group, lesson, etc.)

        :param value: str, The type of the archetype object (group, lesson, etc.)
        :return: None

        """

        self._type = value

    @property
    def description(self) -> str:
        """
        The description of the object.

        :return: str

        """

        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Set the description of the object.

        :param value: str, The description of the object.
        :return: None

        """

        self._description = value


class Lesson(ArchetypeInterface):
    """
    Lesson Model Class

    A Lesson object represents a single lesson to be taught.

    Attributes:
        id (`int`): The Transparent Classroom object id of the group.
        archetype_id (`int`): The id of the archetype.
        name (`str`): The name of the lesson, group, or material being worked.
        lesson_type (`str`): The type of lesson (masterable, ongoing, etc.)
        material (`str`): The material associated with this lesson.
        type (`str`): The type of the archetype object (group, lesson, etc.)
        photo (`str`): The profile photo exemplifying the lesson.
        description (`str`): The description of the object.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            archetype_id: Optional[int] = None,
            name: Optional[str] = None,
            lesson_type: Optional[str] = None,
            material: Optional[str] = None,
            type: Optional[str] = None,
            photo: Optional[str] = None,
            description: Optional[str] = None):
        """
        Lesson Constructor

        :param id: Optional[int], The Transparent Classroom object id of the archetyped object.
        :param archetype_id: Optional[int], The id of the archetype.
        :param name: Optional[str], The name of the lesson, group, or material being worked.
        :param lesson_type: Optional[str], The type of lesson (masterable, ongoing, etc.)
        :param material: Optional[str], The material associated with this lesson.
        :param type: Optional[str], The type of the archetype object (group, lesson, etc.)
        :param photo: Optional[str], The profile photo exemplifying the lesson.
        :param description: Optional[str], The description of the object.
        :return: None

        """

        super().__init__(
            id=id,
            archetype_id=archetype_id,
            name=name,
            type=type,
            description=description
        )
        self.lesson_type = lesson_type
        self.material = material
        self.photo = photo

    @property
    def lesson_type(self) -> str:
        """
        The type of lesson (masterable, ongoing, etc.)

        :return: str

        """

        return self._lesson_type

    @lesson_type.setter
    def lesson_type(self, value: str) -> None:
        """
        Set the type of lesson (masterable, ongoing, etc.)

        :param value: str, The type of lesson (masterable, ongoing, etc.)
        :return: None

        """

        self._lesson_type = value

    @property
    def material(self) -> str:
        """
        The material associated with this lesson.

        :return: str

        """

        return self._material

    @material.setter
    def material(self, value: str) -> None:
        """
        Set the material associated with this lesson.

        :param value: str, The material associated with this lesson.
        :return: None

        """

        self._material = value

    @property
    def photo(self) -> str:
        """
        The profile photo exemplifying the lesson.

        :return: str

        """

        return self._photo

    @photo.setter
    def photo(self, value: str) -> None:
        """
        Set the profile photo exemplifying the lesson.

        :param value: str, The profile photo exemplifying the lesson.
        :return: None

        """

        self._photo = value


class Group(ArchetypeInterface):
    """
    Group Model Class

    A Group object represents a group of lessons in a specific area.

    Attributes:
        id (`int`): The Transparent Classroom object id of the group.
        archetype_id (`int`): The id of the archetype.
        name (`str`): The name of the lesson, group, or material being worked.
        type (`str`): The type of the archetype object (group, lesson, etc.)
        description (`str`): The description of the object.
        subgroups (`List[Group]`): The subgroups defining this lesson set group.
        lessons (`List[Lesson]`): The lessons under this group.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            archetype_id: Optional[int] = None,
            name: Optional[str] = None,
            type: Optional[str] = None,
            description: Optional[str] = None,
            subgroups: List['Group'] = None,
            lessons: List[Lesson] = None) -> None:
        """
        Group Constructor

        :param id: Optional[int], The Transparent Classroom object id of the archetyped object.
        :param archetype_id: Optional[int], The id of the archetype.
        :param name: Optional[str], The name of the lesson, group, or material being worked.
        :param type: Optional[str], The type of the archetype object (group, lesson, etc.)
        :param description: Optional[str], The description of the object.
        :param subgroups: Optional[List[Group]], The groups defining this lesson set group.
        :param lessons: Optional[List[Lesson]], The lessons under this group.
        :return: None

        """

        super().__init__(
            id=id,
            archetype_id=archetype_id,
            name=name,
            type=type,
            description=description
        )
        self.subgroups = subgroups
        self.lessons = lessons

    @property
    def subgroups(self) -> List['Group']:
        """
        The subgroups defining this lesson set area.

        :return: List[Group]

        """

        return self._subgroups

    @subgroups.setter
    def subgroups(self, value: List['Group']) -> None:
        """
        Set the subgroups defining this lesson set area.

        :param value: List[Group], The subgroups defining this lesson set area.
        :return: None

        """

        self._subgroups = [] if value is None else value

    @property
    def lessons(self) -> List['Lesson']:
        """
        The lessons under this group.

        :return: List[Lesson]

        """

        return self._lessons

    @lessons.setter
    def lessons(self, value: List['Lesson']) -> None:
        """
        Set the lessons under this group.

        :param value: List[Lesson], The lessons under this group.
        :return: None

        """

        self._lessons = [] if value is None else value


class Area(ArchetypeInterface):
    """
    Area Model Class

    An Area object represents an area of lessons.

    Attributes:
        id (`int`): The Transparent Classroom object id of the lesson set.
        archetype_id (`int`): The id of the archetype.
        name (`str`): The name of the lesson, group, or material being worked.
        type (`str`): The type of the archetype object (group, lesson, etc.)
        description (`str`): The description of the object.
        groups (`List[Group]`): The groups defining this lesson set area.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            archetype_id: Optional[int] = None,
            name: Optional[str] = None,
            type: Optional[str] = None,
            description: Optional[str] = None,
            groups: List[Group] = None) -> None:
        """
        Area Constructor

        :param id: Optional[int], The Transparent Classroom object id of the archetyped object.
        :param archetype_id: Optional[int], The id of the archetype.
        :param name: Optional[str], The name of the lesson, group, or material being worked.
        :param type: Optional[str], The type of the archetype object (group, lesson, etc.)
        :param description: Optional[str], The description of the object.
        :param groups: Optional[List[Group]], The groups defining this lesson set area.
        :return: None

        """

        super().__init__(
            id=id,
            archetype_id=archetype_id,
            name=name,
            type=type,
            description=description
        )
        self.groups = groups

    @property
    def groups(self) -> List[Group]:
        """
        The groups defining this lesson set area.

        :return: List[Group]

        """

        return self._groups

    @groups.setter
    def groups(self, value: List[Group]) -> None:
        """
        Set the groups defining this lesson set area.

        :param value: List[Group], The groups defining this lesson set area.
        :return: None

        """

        self._groups = [] if value is None else value


class Scale(JSONModel):
    """
    Scale Class

    Attributes:
        name (`str`): The name of the scale.
        values (`List`): The values of the scale/metric.

    """

    def __init__(self, name: Optional[str] = None, values: Optional[List] = None) -> None:
        """
        Scale Constructor

        :param name: Optional[str], The name of the scale.
        :param values: Optional[List], The values of the scale/metric.
        :return: None

        """

        self.name = name
        self.values = values

    @property
    def name(self) -> str:
        """
        The name of the scale.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the scale.

        :param value: str, The name of the scale.
        :return: None

        """

        self._name = value

    @property
    def values(self) -> List[str]:
        """
        The values of the scale/metric.

        :return: List[str]

        """

        return self._values

    @values.setter
    def values(self, value: List[str]) -> None:
        """
        Set the values of the scale/metric.

        :param value: List[str], The values of the scale/metric.
        :return: None

        """

        self._values = [None] * 6 if value is None else value


class LessonSet(Model):
    """
    Lesson Set Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the lesson set.
        name (`str`): The name of the lesson set.
        type (`str`): The lesson set/object type.
        areas (`List[Area]`): The list of lesson set areas associated with this lesson
            set.
        scales (`List[Scale]`): The scales/metrics used for when defining student
            engagement with a specific lesson in the lesson set.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            type: Optional[str] = None,
            areas: Optional[List[Area]] = None,
            scales: Optional[List[Scale]] = None) -> None:
        """
        Lesson Set Constructor

        :param id: Optional[int], The Transparent Classroom object id of the lesson set.
        :param name: Optional[str], The name of the lesson set.
        :param type: Optional[str], lesson set/object type.
        :param areas: Optional[List[Area]], The list of lesson set areas associated with
            this lesson set.
        :param scales: Optional[List[Scale]], scales/metrics used for when defining student
            engagement with a specific lesson in the lesson set.
        :return: None

        """

        super().__init__(id=id)
        self.name = name
        self.type = type
        self.areas = areas
        self.scales = scales

    @property
    def name(self) -> str:
        """
        The name of the lesson set.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the lesson set.

        :param value: str, The name of the lesson set.
        :return: None

        """

        self._name = value

    @property
    def type(self) -> str:
        """
        The lesson set/object type.

        :return: str

        """

        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """
        Set the lesson set/object type.

        :param value: str, The lesson set/object type.
        :return: None

        """

        self._type = value

    @property
    def areas(self) -> List[Area]:
        """
        The children lesson sets/lessons.

        :return: List[Area]

        """

        return self._areas

    @areas.setter
    def areas(self, value: List[Area]) -> None:
        """
        Set the children lesson sets/lessons.

        :param value: List[Area], The children lesson sets/lessons.
        :return: None

        """

        self._areas = [] if value is None else value

    @property
    def scales(self) -> List[Scale]:
        """
        The scales/metrics used for when defining student engagement with a
            specific lesson in the lesson set.

        :return: List[Scale]

        """

        return self._scales

    @scales.setter
    def scales(self, value: List[Scale]) -> None:
        """
        Set the scales/metrics used for when defining student engagement with a
            specific lesson in the lesson set.

        :param value: List[Scale], The scales/metrics used for when defining student
            engagement with a specific lesson in the lesson set.
        :return: None

        """

        self._scales = [] if value is None else value


class Level(JSONModel):
    """
    Level Model Class

    Attributes:
        child_id (`int`): The id of the child associated with this lesson's proficiency level.
        lesson_id (`int`): The id of the lesson given to the child for the level assessment.
        proficiency (`int`): The proficiency score assessed to the student on the lesson.
        date (`date`): The date the lesson was given and the level assessment was made.
        planned (`bool`): Flag indicating whether the lesson/assessment was planned.

    """

    def __init__(
            self,
            child_id: Optional[int] = None,
            lesson_id: Optional[int] = None,
            proficiency: Optional[int] = None,
            date: Optional[Union[datetime.date, str]] = None,
            planned: Optional[bool] = None) -> None:
        """
        Level Constructor

        :param child_id: Optional[int], The id of the child associated with this lesson's proficiency level.
        :param lesson_id: Optional[int], The id of the lesson given to the child for the level assessment.
        :param proficiency: Optional[int], The proficiency score assessed to the student on the lesson.
        :param date: Optional[Union[date, str]], The date the lesson was given and the level assessment was made.
        :param planned: Optional[bool], Flag indicating whether the lesson/assessment was planned.
        :return: None

        """

        self.child_id = child_id
        self.lesson_id = lesson_id
        self.proficiency = proficiency
        self.date = date
        self.planned = planned

    @property
    def child_id(self) -> int:
        """
        The id of the child associated with this lesson's proficiency level.

        :return: int

        """

        return self._child_id

    @child_id.setter
    def child_id(self, value: int) -> None:
        """
        Set the id of the child associated with this lesson's proficiency level.

        :param value: int, The id of the child associated with this lesson's proficiency level.
        :return: None

        """

        self._child_id = value

    @property
    def lesson_id(self) -> int:
        """
        The id of the lesson given to the child for the level assessment.

        :return: int

        """

        return self._lesson_id

    @lesson_id.setter
    def lesson_id(self, value: int) -> None:
        """
        Set the id of the lesson given to the child for the level assessment.

        :param value: int, The id of the lesson given to the child for the level assessment.
        :return: None

        """

        self._lesson_id = value

    @property
    def proficiency(self) -> int:
        """
        The proficiency score assessed to the student on the lesson.

        :return: int

        """

        return self._proficiency

    @proficiency.setter
    def proficiency(self, value: int) -> None:
        """
        Set the proficiency score assessed to the student on the lesson.

        :param value: int, The proficiency score assessed to the student on the lesson.
        :return: None

        """

        self._proficiency = value

    @property
    def date(self) -> datetime.date:
        """
        The date the lesson was given and the level assessment was made.

        :return: date

        """

        return self._date

    @date.setter
    def date(self, value: Union[datetime.date, str]) -> None:
        """
        Set the date the lesson was given and the level assessment was made.

        :param value: Union[date, str], The date the lesson was given and the level assessment was made.
        :return: None

        """

        self._date = Formatter.str_to_date(value=value)

    @property
    def planned(self) -> bool:
        """
        The flag indicating whether the lesson/assessment was planned.

        :return: bool

        """

        return self._planned

    @planned.setter
    def planned(self, value: bool) -> None:
        """
        Set the flag indicating whether the lesson/assessment was planned.

        :param value: bool, The flag indicating whether the lesson/assessment was planned.
        :return: None

        """

        self._planned = value


class OnlineApplication(Model):
    """
    Online Application Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the online application.
        school_id (`int`): The id of the school that the child/family is applying to.
        type (`str`): The type of form/application.
        state (`str`): The submission state of the online application.
        fields (`Dict`): The question-answer responses provided by the respondent on the form.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            school_id: Optional[int] = None,
            type: Optional[str] = None,
            state: Optional[str] = None,
            fields: Optional[List[Widget]] = None) -> None:
        """
        Online Application Constructor

        :param id: Optional[int], The Transparent Classroom object id of the online application.
        :param school_id: Optional[int], The id of the school that the child/family is applying to.
        :param type: Optional[str], The type of form/application.
        :param state: Optional[str], The submission state of the online application.
        :param fields: Optional[List[Widget]], The question-answer responses provided by the respondent on
            the form.
        :return: None

        """

        super().__init__(id=id)
        self.school_id = school_id
        self.type = type
        self.state = state
        self.fields = fields

    @property
    def school_id(self) -> int:
        """
        The id of the school that the child/family is applying to.

        :return: int

        """

        return self._school_id

    @school_id.setter
    def school_id(self, value: int) -> None:
        """
        Set the id of the school that the child/family is applying to.

        :param value: str, The id of the school that the child/family is applying to.
        :return: None

        """

        self._school_id = value

    @property
    def type(self) -> str:
        """
        The type of form/application.

        :return: str

        """

        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """
        Set the type of form/application.

        :param value: str, The
        :return: None

        """

        self._type = value

    @property
    def state(self) -> str:
        """
        The submission state of the online application.

        :return: str

        """

        return self._state

    @state.setter
    def state(self, value: str) -> None:
        """
        Set the submission state of the online application.

        :param value: str, The submission state of the online application.
        :return: None

        """

        self._state = value

    @property
    def fields(self) -> List[Widget]:
        """
        The question-answer responses provided by the respondent on the form.

        :return: List[Widget]

        """

        return self._fields

    @fields.setter
    def fields(self, value: List[Widget]) -> None:
        """
        Set the question-answer responses provided by the respondent on the form.

        :param value: List[Widget], The question-answer responses provided by the respondent
            on the form.
        :return: None

        """

        self._fields = [] if value is None else value


class School(Model):
    """
    School Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the school.
        name (`str`): The name of the school.
        phone (`str`): The phone number of the school.
        address (`str`): The street address of the school.
        type (`str`): The type of school/entity (school, network, etc.).
        timezone (`str`): The timezone that the school is located in.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            phone: Optional[str] = None,
            address: Optional[str] = None,
            type: Optional[str] = None,
            timezone: Optional[str] = None) -> None:
        """
        School Constructor

        :param id: Optional[int], The Transparent Classroom object id of the school.
        :param name: Optional[str], The name of the school.
        :param phone: Optional[str], The phone number of the school.
        :param address: Optional[str], The street address of the school.
        :param type: Optional[str], The type of school/entity (school, network, etc.).
        :param timezone: Optional[str], The timezone that the school is located in.
        :return: None

        """

        super().__init__(id=id)
        self.name = name
        self.phone = phone
        self.address = address
        self.type = type
        self.timezone = timezone

    @property
    def name(self) -> str:
        """
        The name of the school.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the school.

        :param value: str, The name of the school.
        :return: None

        """

        self._name = value

    @property
    def phone(self) -> str:
        """
        The phone number of the school.

        :return: str

        """

        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """
        Set the phone number of the school.

        :param value: str, The phone number of the school.
        :return: None

        """

        self._phone = value

    @property
    def address(self) -> str:
        """
        The street address of the school.

        :return: str

        """

        return self._address

    @address.setter
    def address(self, value: str) -> None:
        """
        Set the street address of the school.

        :param value: str, The street address of the school.
        :return: None

        """

        self._address = value

    @property
    def type(self) -> str:
        """
        The type of school/entity (school, network, etc.).

        :return: str

        """

        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """
        Set the type of school/entity (school, network, etc.).

        :param value: str, The type of school/entity (school, network, etc.).
        :return: None

        """

        self._type = value

    @property
    def timezone(self) -> str:
        """
        The timezone that the school is located in.

        :return: str

        """

        return self._timezone

    @timezone.setter
    def timezone(self, value: str) -> None:
        """
        Set the timezone that the school is located in.

        :param value: str, The timezone that the school is located in.
        :return: None

        """

        self._timezone = value


class Session(Model):
    """
    Session Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the session.
        name (`str`): The name of the instruction session.
        start_date (`date`): The start date of the session of instruction.
        stop_date (`date`): The stop date of the session of instruction.
        children (`int`): The number of children enrolled during the session.
        current (`bool`): Flag indicating whether it is the current session.
        inactive (`bool`): Flag indicating whether the session is inactive.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            start_date: Optional[Union[datetime.date, str]] = None,
            stop_date: Optional[Union[datetime.date, str]] = None,
            children: Optional[int] = None,
            current: Optional[bool] = None,
            inactive: Optional[bool] = None) -> None:
        """
        Session Constructor

        :param id: Optional[int], The Transparent Classroom object id of the session.
        :param name: Optional[str], The name of the instruction session.
        :param start_date: Optional[Union[date, str]], The start date of the session of instruction.
        :param stop_date: Optional[Union[date, str]], The stop date of the session of instruction.
        :param children: Optional[int], The number of children enrolled during the session.
        :param current: Optional[bool], Flag indicating whether it is the current session.
        :param inactive: Optional[bool], Flag indicating whether the session is inactive.
        :return: None

        """

        super().__init__(id=id)
        self.name = name
        self.start_date = start_date
        self.stop_date = stop_date
        self.children = children
        self.current = current
        self.inactive = inactive

    @property
    def name(self) -> str:
        """
        The name of the instruction session.

        :return: str

        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the instruction session.

        :param value: str, The name of the instruction session.
        :return: None

        """

        self._name = value

    @property
    def start_date(self) -> datetime.date:
        """
        The start date of the session of instruction.

        :return: date

        """

        return self._start_date

    @start_date.setter
    def start_date(self, value: Union[datetime.date, str]) -> None:
        """
        Set the start date of the session of instruction.

        :param value: Union[date, str], The start date of the session of instruction.
        :return: None

        """

        self._start_date = Formatter.str_to_date(value=value)

    @property
    def stop_date(self) -> datetime.date:
        """
        The end date of the session of instruction.

        :return: date

        """

        return self._stop_date

    @stop_date.setter
    def stop_date(self, value: Union[datetime.date, str]) -> None:
        """
        Set the end date of the session of instruction.

        :param value: Union[date, str], The end date of the session of instruction.
        :return: None

        """

        self._stop_date = Formatter.str_to_date(value=value)

    @property
    def children(self) -> int:
        """
        The number of children enrolled during the session.

        :return: int

        """

        return self._children

    @children.setter
    def children(self, value: int) -> None:
        """
        Set the number of children enrolled during the session.

        :param value: int, The number of children enrolled during the session.
        :return: None

        """

        self._children = value

    @property
    def current(self) -> bool:
        """
        The flag indicating whether it is the current session.

        :return: bool

        """

        return self._current

    @current.setter
    def current(self, value: bool) -> None:
        """
        Set the flag indicating whether it is the current session.

        :param value: bool, The flag indicating whether it is the current session.
        :return: None

        """

        self._current = value

    @property
    def inactive(self) -> bool:
        """
        The flag indicating whether the session is inactive.

        :return: bool

        """

        return self._inactive

    @inactive.setter
    def inactive(self, value: bool) -> None:
        """
        Set the flag indicating whether the session is inactive.

        :param value: bool, The flag indicating whether the session is inactive.
        :return: None

        """

        self._inactive = value


class User(Model):
    """
    User Model Class

    Attributes:
        id (`int`): The Transparent Classroom object id of the user.
        type (`str`): The type of user (user, admin, etc.)
        inactive (`bool`): Flag indicating whether the user account is inactive.
        email (`str`): The email address associated with the user account.
        first_name (`str`): The first name of the user.
        last_name (`str`): The last name of the user.
        roles (`List[str]`): The roles held by the user (teacher, admin, etc.)
        accessible_classroom_ids (`List[int]`): The list of classroom ids that the
            use has access to.
        default_classroom_id (`int`): The id of the classroom associated with the
            user by default (e.g. The id of the teacher's classroom).
        street (`str`): The street address of the user.
        postal_code (`str`): The postal code of the area the user is in.
        city (`str`): The city that the user is located in.
        state_province (`str`): The state/province that the user is located in.
        home_number (`str`): The home phone number of the user.
        mobile_number (`str`): The mobile phone number of the user.
        work_number (`str`): The work phone number of the user.

    """

    def __init__(
            self,
            id: Optional[int] = None,
            type: Optional[str] = None,
            inactive: Optional[bool] = None,
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            roles: Optional[List[str]] = None,
            accessible_classroom_ids: Optional[List[int]] = None,
            default_classroom_id: Optional[int] = None,
            street: Optional[str] = None,
            postal_code: Optional[str] = None,
            city: Optional[str] = None,
            state_province: Optional[str] = None,
            home_number: Optional[str] = None,
            mobile_number: Optional[str] = None,
            work_number: Optional[str] = None) -> None:
        """
        User Constructor

        :param id: Optional[int], The Transparent Classroom object id of the user.
        :param type: Optional[str], The type of user (user, admin, etc.)
        :param inactive: Optional[bool], Flag indicating whether the user account is inactive.
        :param email: Optional[str], The email address associated with the user account.
        :param first_name: Optional[str], The first name of the user.
        :param last_name: Optional[str], The last name of the user.
        :param roles: Optional[List[str]], The roles held by the user (teacher, admin, etc.)
        :param accessible_classroom_ids: Optional[List[int]], The list of classroom ids that the
            use has access to.
        :param default_classroom_id: Optional[int], The id of the classroom associated with the
            user by default (e.g. The id of the teacher's classroom).
        :param street: Optional[str], The street address of the user.
        :param postal_code: Optional[str], The postal code of the area the user is in.
        :param city: Optional[str], The city that the user is located in.
        :param state_province: Optional[str], The state/province that the user is located in.
        :param home_number: Optional[str], The home phone number of the user.
        :param mobile_number: Optional[str], The mobile phone number of the user.
        :param work_number: Optional[str], The work phone number of the user.
        :return: None

        """

        super().__init__(id=id)
        self.type = type
        self.inactive = inactive
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.roles = roles
        self.accessible_classroom_ids = accessible_classroom_ids
        self.default_classroom_id = default_classroom_id
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.state_province = state_province
        self.home_number = home_number
        self.mobile_number = mobile_number
        self.work_number = work_number

    @property
    def type(self) -> str:
        """
        The type of user (user, admin, etc.)

        :return: str

        """

        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """
        Set the type of user (user, admin, etc.)

        :param value: str, The type of user (user, admin, etc.)
        :return: None

        """

        self._type = value

    @property
    def inactive(self) -> bool:
        """
        Flag indicating whether the user account is inactive.

        :return: bool

        """

        return self._inactive

    @inactive.setter
    def inactive(self, value: bool) -> None:
        """
        Set the flag indicating whether the user account is inactive.

        :param value: bool, The flag indicating whether the user account is inactive.
        :return: None

        """

        self._inactive = value

    @property
    def email(self) -> str:
        """
        The email address associated with the user account.

        :return: str

        """

        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """
        Set the email address associated with the user account.

        :param value: str, The email address associated with the user account.
        :return: None

        """

        self._email = value

    @property
    def first_name(self) -> str:
        """
        The first name of the user.

        :return: str

        """

        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Set the first name of the user.

        :param value: str, The last name of the user.
        :return: None

        """

        self._first_name = value

    @property
    def last_name(self) -> str:
        """
        The last name of the user.

        :return: str

        """

        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Set the last name of the user.

        :param value: str, The last name of the user.
        :return: None

        """

        self._last_name = value

    @property
    def roles(self) -> List[str]:
        """
        The roles held by the user (teacher, admin, etc.)

        :return: List[str]

        """

        return self._roles

    @roles.setter
    def roles(self, value: List[str]) -> None:
        """
        Set the roles held by the user (teacher, admin, etc.)

        :param value: List[str], The roles held by the user (teacher, admin, etc.)
        :return: None

        """

        self._roles = value

    @property
    def accessible_classroom_ids(self) -> List[int]:
        """
        The list of classroom ids that the use has access to.

        :return: List[int]

        """

        return self._accessible_classroom_ids

    @accessible_classroom_ids.setter
    def accessible_classroom_ids(self, value: List[int]) -> None:
        """
        Set the list of classroom ids that the use has access to.

        :param value: List[int], The list of classroom ids that the use has access to.
        :return: None

        """

        self._accessible_classroom_ids = value

    @property
    def default_classroom_id(self) -> int:
        """
        The id of the classroom associated with the user by default (e.g. The
        id of the teacher's classroom).

        :return: int

        """

        return self._default_classroom_id

    @default_classroom_id.setter
    def default_classroom_id(self, value: int) -> None:
        """
        Set the default classroom id of the user.

        :param value: int, The default classroom id of the user.
        :return: None

        """

        self._default_classroom_id = value

    @property
    def street(self) -> str:
        """
        The street address of the user.

        :return: str

        """

        return self._street

    @street.setter
    def street(self, value: str) -> None:
        """
        Set the street address of the user.

        :param value: str, The street address of the user.
        :return: None

        """

        self._street = value

    @property
    def city(self) -> str:
        """
        The city that the user is located in.

        :return: str

        """

        return self._city

    @city.setter
    def city(self, value: str) -> None:
        """
        Set the city that the user is located in.

        :param value: str, The city that the user is located in.
        :return: None

        """

        self._city = value

    @property
    def postal_code(self) -> str:
        """
        The postal code of the area the user is in.

        :return: str

        """

        return self._postal_code

    @postal_code.setter
    def postal_code(self, value: str) -> None:
        """
        Set the postal code of the area the user is in.

        :param value: str, The postal code of the area the user is in.
        :return: None

        """

        self._postal_code = value

    @property
    def state_province(self) -> str:
        """
        The state/province that the user is located in.

        :return: str

        """

        return self._state_province

    @state_province.setter
    def state_province(self, value: str) -> None:
        """
        Set the state/province that the user is located in.

        :param value: str, The state/province that the user is located in.
        :return: None

        """

        self._state_province = value

    @property
    def home_number(self) -> str:
        """
        The home phone number of the user.

        :return: str

        """

        return self._home_number

    @home_number.setter
    def home_number(self, value: str) -> None:
        """
        Set the home phone number of the user.

        :param value: str, The home phone number of the user.
        :return: None

        """

        self._home_number = value

    @property
    def mobile_number(self) -> str:
        """
        The mobile phone number of the user.

        :return: str

        """

        return self._mobile_number

    @mobile_number.setter
    def mobile_number(self, value: str) -> None:
        """
        Set the mobile phone number of the user.

        :param value: str, The mobile phone number of the user.
        :return: None

        """

        self._mobile_number = value

    @property
    def work_number(self) -> str:
        """
        The work phone number of the user.

        :return: str

        """

        return self._work_number

    @work_number.setter
    def work_number(self, value: str) -> None:
        """
        Set the work phone number of the user.

        :param value: str, The work phone number of the user.
        :return: None

        """

        self._work_number = value


class Auth(JSONModel):
    """
    Auth Model Class

    This class represents the response object received from an authentication request to
    the Transparent Classroom's auth endpoint.

    Attributes:
        school_id (`int`): The id of the school that the use is authenticated to access.
        api_token (`str`): The authentication token received from Transparent Classroom
            to use when submitting API requests to TC.
        push_tokens (`List`): Tokens to use for sending push notifications.
        push_enabled (`bool`): Flag indicating whether push notifications are enabled
            for the specified auth setting.
        user (`User`): The user associated with the authentication request.

    """

    def __init__(
            self,
            school_id: Optional[int] = None,
            api_token: Optional[str] = None,
            push_tokens: Optional[List] = None,
            push_enabled: Optional[bool] = None,
            user: Optional[User] = None) -> None:
        """
        Auth Model Constructor

        :param school_id: Optional[int], The id of the school that the use is authenticated
            to access.
        :param api_token: Optional[str], The authentication token received from Transparent
            Classroom to use when submitting API requests to TC.
        :param push_tokens: Optional[List], Tokens to use for sending push notifications.
        :param push_enabled: Optional[bool], Flag indicating whether push notifications are
            enabled for the specified auth setting.
        :param user: Optional[User], The user associated with the authentication request.
        :return: None

        """

        self.school_id = school_id
        self.api_token = api_token
        self.push_tokens = push_tokens
        self.push_enabled = push_enabled
        self.user = user

    @property
    def school_id(self) -> int:
        """
        The id of the school that the use is authenticated to access.

        :return: int

        """

        return self._school_id

    @school_id.setter
    def school_id(self, value: int) -> None:
        """
        Set the id of the school that the use is authenticated to access.

        :param value: int, The id of the school that the use is authenticated to access.
        :return: None

        """

        self._school_id = value

    @property
    def api_token(self) -> str:
        """
        The authentication token received from Transparent Classroom to use when submitting
        API requests to TC.

        :return: str

        """

        return self._api_token

    @api_token.setter
    def api_token(self, value: str) -> None:
        """
        Set the authentication token received from Transparent Classroom to use when
        submitting API requests to TC.

        :param value: str, The authentication token received from Transparent Classroom to
            use when submitting API requests to TC.
        :return: None

        """

        self._api_token = value

    @property
    def push_tokens(self) -> List:
        """
        The tokens to use for sending push notifications.

        :return: List

        """

        return self._push_tokens

    @push_tokens.setter
    def push_tokens(self, value: List) -> None:
        """
        Set the tokens to use for sending push notifications.

        :param value: List, The tokens to use for sending push notifications.
        :return: None

        """

        self._push_tokens = value

    @property
    def push_enabled(self) -> bool:
        """
        The flag indicating whether push notifications are enabled for the specified
        auth setting.

        :return: bool

        """

        return self._push_enabled

    @push_enabled.setter
    def push_enabled(self, value: bool) -> None:
        """
        Set the flag indicating whether push notifications are enabled for the specified
        auth setting.

        :param value: bool, The flag indicating whether push notifications are enabled
            for the specified auth setting.
        :return: None

        """

        self._push_enabled = value

    @property
    def user(self) -> User:
        """
        The user associated with the authentication request.

        :return: User

        """

        return self._user

    @user.setter
    def user(self, value: User) -> None:
        """
        Set the user associated with the authentication request.

        :param value: User, The user associated with the authentication request.
        :return: None

        """

        self._user = value
