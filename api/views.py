import uuid

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .authentication import ApiKeyAuthentication
from .models import ApiKey, News
from .serializers import ApiKeySerializer, NewsSerializer, UserSerializer
from .throttles import BurstRateThrottle, DailyRateThrottle

# Create your views here.


class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "per_page"
    max_page_size = 50


@extend_schema(
    summary="Gerar chave de API",
    description="Cria uma nova chave de API para o usuário com base no email fornecido",
    request=UserSerializer,
    responses={201: ApiKeySerializer},
    tags=["Authentication"],
)
class CreateAPIkeyView(generics.GenericAPIView):
    """
    Criar a apikey do usuario e retorna
    """

    serializer_class = UserSerializer
    throttle_classes = [BurstRateThrottle, DailyRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["email"],
            email=serializer.validated_data["email"],
        )

        api_key = uuid.uuid4().hex
        ApiKey.objects.create(user=user, api_key=api_key)

        return Response(
            {
                "api_key": api_key,
                "user_id": user.id,
                "message": "API Key criada com sucesso!",
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    summary="Busca noticia",
    parameters=[
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Busca noticia por palavra-chave",
            required=True,
        )
    ],
)
class SearchNewsView(generics.ListAPIView):
    """
    Buscar notícias por palavra-chave

    Permite buscar notícias usando termos no título e descrição.
    Rate limit: 100 requests/hora
    """

    throttle_classes = [BurstRateThrottle, DailyRateThrottle]
    authentication_classes = [ApiKeyAuthentication]
    serializer_class = NewsSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]
    pagination_class = NewsPagination

    def get_queryset(self):
        return News.objects.all()

    @method_decorator(cache_page(300, key_prefix="search_news"), name="dispatch")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return response


@extend_schema(
    summary="Filtra por categoria",
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filtra por categoria a noticia",
            required=True,
            enum=["geral", "tecnologia", "esportes", "negócios"],
        )
    ],
)
class CategoryNewsView(generics.ListAPIView):
    """
    Filtra notícias por categoria,
    Rate limit: 100 requests/hora
    """

    throttle_classes = [BurstRateThrottle, DailyRateThrottle]
    authentication_classes = [ApiKeyAuthentication]
    serializer_class = NewsSerializer
    pagination_class = NewsPagination

    def get_queryset(self):
        VALID_CATEGORIES = ["geral", "tecnologia", "esportes", "negócios"]
        category = self.request.query_params.get("category")

        if not category:
            raise ValidationError(
                {
                    "error": "Parâmetro 'category' é obrigatório",
                    "valid_categories": VALID_CATEGORIES,
                }
            )
        if category not in VALID_CATEGORIES:
            raise ValidationError(
                {
                    "error": f"Categoria '{category}' não existe",
                    "valid_categories": VALID_CATEGORIES,
                    "received": category,
                }
            )

        return News.objects.filter(category=category)

    @method_decorator(cache_page(300, key_prefix="category_news"), name="dispatch")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return response
