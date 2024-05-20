from transparent_classroom.api.routing.routes import RouteComponent


# Route component included in all API paths
API_V1_ROUTE_COMPONENT = RouteComponent(sub_path="api/v1")

# Route component for specifying the model (e.g. activity, children, etc.)
MODEL_ROUTE_COMPONENT = RouteComponent(sub_path="{{ model_name }}")

# Route component for specifying the object id of a given model in the path
OBJECT_ID_ROUTE_COMPONENT = RouteComponent(sub_path="{{ object_id }}")

# Miscellaneous routes for one-off endpoints
ACCEPT_APPLICATION_ROUTE_COMPONENT = RouteComponent(sub_path="accept_application")
FILTER_LEVELS_BY_DATE_ROUTE_COMPONENT = RouteComponent(sub_path="by_date")
