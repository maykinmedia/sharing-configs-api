from django.urls import include, path

from drf_spectacular.views import SpectacularRedocView, SpectacularYAMLAPIView

from .views import FileDetailView, FileListView

urlpatterns = [
    path(
        "v1/",
        include(
            [
                # API schema
                path(
                    "schema/openapi.yaml",
                    SpectacularYAMLAPIView.as_view(),
                    name="schema",
                ),
                path(
                    "schema/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="schema-redoc",
                ),
                # API endpoints
                path(
                    "config/<str:slug>/folder/<str:folder>/files/<str:filename>/",
                    FileDetailView.as_view(),
                    name="file-detail",
                ),
                path(
                    "config/<str:slug>/folder/<str:folder>/files/",
                    FileListView.as_view(),
                    name="file-list",
                ),
            ]
        ),
    ),
]
