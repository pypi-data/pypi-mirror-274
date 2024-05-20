from enum import Enum


class ModelType(Enum):
    """
    Model Type Enum Class

    The available model endpoints provided by the Transparent Classroom API.

    Attributes:


    """

    """
    The model used for accessing teacher/staff activities with the learners. 
    
    """
    ACTIVITY = "activity"

    """
    The model used for user authentication.
    
    """
    AUTHENTICATE = "authenticate"

    """
    The model used to record attributes about the children/learners at the school.
    
    """
    CHILDREN = "children"

    """
    The model used to aggregate classrooms of students, staff, lesson sets, etc.
    
    """
    CLASSROOMS = "classrooms"

    """
    The model used for recording the details of learner conference reports created by staff.
    
    """
    CONFERENCE_REPORTS = "conference_reports"

    """
    The model used to record classroom/student events.
    
    """
    EVENTS = "events"

    """
    The model used to record Transparent Classroom form details.
    
    """
    FORMS = "forms"

    """
    The model used to record Transparent Classroom form template details.

    """
    FORM_TEMPLATES = "form_templates"

    """
    The model used to aggregate sets of lessons for a classroom. 
    
    """
    LESSON_SETS = "lesson_sets"

    """
    The model used to record learner proficiency in a given lesson/subject.
    
    """
    LEVELS = "levels"

    """
    The model used for applications to the school by families.
    
    """
    ONLINE_APPLICATIONS = "online_applications"

    """
    The model used for schools within a network of schools.
    
    """
    SCHOOLS = "schools"

    """
    The model used for school sessions/terms of classes.
    
    """
    SESSIONS = "sessions"

    """
    The model used authentication, roles, platform user details, etc.
    
    """
    USERS = "users"


class EndpointBehavior(Enum):
    """
    Endpoint Behavior Enum Class

    Attributes:


    """

    """
    Accept and Create Child (and Parent). Changes state of application to "Accepted", 
    creates a child, assigns child to classroom, and attaches application to child.

    """
    ACCEPT = "ACCEPT"

    """
    The endpoint will list the associated route objects.

    """
    LIST = "LIST"

    """
    The endpoint will show the object details.

    """
    SHOW = "SHOW"

    """
    The endpoint will show all records associated with a given object (the object
    reference is passed in as a parameter during the request).

    """
    SHOW_ALL = "SHOW_ALL"

    """
    The endpoint will show records filtered by some criteria.

    """
    SHOW_FILTERED = "SHOW_FILTERED"

    """
    Submit an application.

    """
    SUBMIT = "SUBMIT"

    """
    The endpoint will update a record.

    """
    UPDATE = "UPDATE"


class HTTPMethod(Enum):
    """
    HTTP Method Enum Class

    Enum containing the various valid HTTP methods.

    Attributes:


    """

    """
    The HTTP CONNECT method starts two-way communications with the requested resource.
    
    """
    CONNECT = "CONNECT"

    """
    The DELETE method requests that the origin server remove the association between the target 
    resource and its current functionality. . i.e. HTTP DELETE method deletes the specified resource 
    at the origin of server.
    
    """
    DELETE = "DELETE"

    """
    The GET method means retrieve whatever information (in the form of an entity) is identified by the 
    Request-URI.
    
    """
    GET = "GET"

    """
    The HTTP HEAD method requests the headers that would be returned if the HEAD request's URL was 
    instead requested with the HTTP GET method. For example, if a URL might produce a large download, 
    a HEAD request could read its Content-Length header to check the filesize without actually 
    downloading the file.
    
    """
    HEAD = "HEAD"

    """
    The OPTIONS method represents a request for information about the communication options available 
    on the request/response chain identified by the Request-URI.
    
    """
    OPTIONS = "OPTIONS"

    """
    In computing, the PATCH method is a request method in HTTP for making partial changes to an existing 
    resource. The PATCH method provides an entity containing a list of changes to be applied to the 
    resource requested using the HTTP Uniform Resource Identifier (URI).
    
    """
    PATCH = "PATCH"

    """
    The POST request method requests that a web server accept the data enclosed in the body of the request 
    message, most likely for storing it.[1] It is often used when uploading a file or when submitting a 
    completed web form.
    
    """
    POST = "POST"

    """
    The HTTP PUT method is used to create a new resource or replace a resource. It's similar to the POST 
    method, in that it sends data to a server, but it's idempotent. This means that the effect of multiple 
    PUT requests should be the same as one PUT request.
    
    """
    PUT = "PUT"

    """
    TRACE allows the client to see what is being received at the other end of the request chain and use 
    that data for testing or diagnostic information. The value of the Via header field (section 14.45) 
    is of particular interest, since it acts as a trace of the request chain.
    
    """
    TRACE = "TRACE"
