from sharing.api.handlers import BaseHandler

from .service import create_file, get_file, get_files_in_folder


class GitHubHandler(BaseHandler):
    def download(self, folder: str, filename: str) -> bytes:
        github_file = get_file(self.config, folder, filename)
        return github_file.decoded_content

    def upload(self, folder: str, filename: str, content: bytes):
        create_file(self.config, folder, filename, content)

    def list_files(self, folder: str):
        content_files = get_files_in_folder(self.config, folder)
        return [file.name for file in content_files]
