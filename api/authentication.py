from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import ApiKey


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.GET.get("api_key")

        if not api_key:
            raise AuthenticationFailed({"error": "API key obrigatoria"})

        try:
            api_key_obj = ApiKey.objects.get(api_key=api_key)
        except:
            raise AuthenticationFailed({"error": "API key Invalida"})

        return (api_key_obj.user, None)
