from django.urls import include, path

from drf_spectacular.views import SpectacularRedocView, SpectacularYAMLAPIView

from .views import ConfigListView, FileDetailView, FileListView, FolderView

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
                    "config/<str:label>/folder/<path:folder>/files/<str:filename>",
                    FileDetailView.as_view(),
                    name="file-download",
                ),
                path(
                    "config/<str:label>/folder/<path:folder>/files/",
                    FileListView.as_view(),
                    name="file-list",
                ),
                path(
                    "config/<str:label>/folder/",
                    FolderView.as_view(),
                    name="folder-root",
                ),
                path("configs/", ConfigListView.as_view(), name="config-list"),
            ]
        ),
    ),
]
