from github import GithubException, UnknownObjectException

from sharing.core.constants import ConfigTypes
from sharing.core.exceptions import HandlerException, HandlerObjectNotFound
from sharing.core.handlers import BaseHandler

from .service import (
    create_file,
    get_file,
    get_files_in_folder,
    get_folders,
    update_file,
)


def github_error_handler(func):
    """catch github specific exceptions and raise base handler errors"""

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

        except UnknownObjectException as exc:
            details = exc.data.get("message", "Not Found")
            raise HandlerObjectNotFound(f"Github Error: {details}")
        except GithubException as exc:
            details = exc.data.get("message", "Connection can't be established")
            raise HandlerException(f"Github Error: {details}")

        return result

    return wrapper


class GitHubHandler(BaseHandler, type=ConfigTypes.github):
    @github_error_handler
    def download(self, folder: str, filename: str) -> bytes:
        github_file = get_file(self.config, folder, filename)
        return github_file.decoded_content

    @github_error_handler
    def upload(
        self,
        folder: str,
        filename: str,
        content: bytes,
        comment: str,
        overwrite: bool = False,
    ):
        folder_files = self.list_files(folder)
        if filename in folder_files:
            if not overwrite:
                raise HandlerException(
                    f"File {filename} already exists in the folder. "
                    "Use 'overwrite' attribute if you want to replace it"
                )

            return update_file(self.config, folder, filename, content, comment)

        return create_file(self.config, folder, filename, content, comment)

    @github_error_handler
    def list_files(self, folder: str):
        content_files = get_files_in_folder(self.config, folder)
        return [file.name for file in content_files]

    @github_error_handler
    def list_folders(self):
        return get_folders(self.config)
