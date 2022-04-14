from rest_framework.permissions import SAFE_METHODS, BasePermission

from .constants import PermissionModes


class IsTokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.auth)


class RootPathPermission(BasePermission):
    def has_permission(self, request, view):
        label = view.kwargs["label"]
        folder = view.kwargs.get("folder")

        if not label or not folder:
            return True

        config = request.auth.configs.all().filter(label=label).first()
        if not config:
            # in the view it will raise 404 error
            return True

        root_folder = folder.split("/")[0]
        root_path_config = config.root_paths.all().filter(folder=root_folder).first()
        if not root_path_config:
            return False

        return self.check_root_path(request, root_path_config)

    def check_root_path(self, request, root_path_config) -> bool:
        """check if root path permission is sufficient"""
        if request.method in SAFE_METHODS:
            return True

        return bool(root_path_config.permission == PermissionModes.write)
