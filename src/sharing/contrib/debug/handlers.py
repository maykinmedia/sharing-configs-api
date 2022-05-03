import logging

from sharing.core.data import Folder
from sharing.core.handlers import BaseHandler

logger = logging.getLogger(__name__)


class DebugHandler(BaseHandler, type="debug"):
    """handler used for testing, It downloads the example file and uploads file into stdout"""

    def download(self, folder: str, filename: str):
        return b"example file"

    def upload(
        self,
        folder: str,
        filename: str,
        content: bytes,
        comment: str,
        overwrite: bool = False,
    ):
        logger.info(f"DebugHandler: {comment}")

    def list_files(self, folder: str):
        return ["example_file.txt"]

    def list_folders(self):
        return [
            Folder(
                name="example_folder",
                children=[
                    Folder(name="example_subfolder"),
                ],
            ),
            Folder(name="example_other_folder"),
        ]
