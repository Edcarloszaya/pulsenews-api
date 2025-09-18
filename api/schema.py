# api/schema.py
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class ApiKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = (
        "api.authentication.ApiKeyAuthentication"  
    )
    name = "ApiKeyAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "query",  
            "name": "api_key",
        }
