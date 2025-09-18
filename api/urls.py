from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import CategoryNewsView, CreateAPIkeyView, SearchNewsView

urlpatterns = [
    path("create-api-key/", CreateAPIkeyView.as_view(), name="create-api-key"),
    path("news/", SearchNewsView.as_view(), name="search_news"),
    path("news/category/", CategoryNewsView.as_view(), name="category_news"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
