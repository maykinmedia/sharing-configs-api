import logging
import os.path
from typing import List

from github import ContentFile, Github, GithubObject

from sharing.core.models import Config

logger = logging.getLogger(__name__)


def get_file(config: Config, folder: str, filename: str) -> ContentFile.ContentFile:
    """
    Return the content of the file

    :calls: `GET /repos/{owner}/{repo}/contents/{path}
    """
    g = Github(config.access_token)
    repo = g.get_repo(config.repo)
    branch = config.branch or GithubObject.NotSet

    file_path = os.path.join(folder, filename)

    return repo.get_contents(path=file_path, ref=branch)


def create_file(
    config: Config, folder: str, filename: str, content: bytes, comment: str = None
) -> ContentFile.ContentFile:
    """
    Create file in the repo

    :calls: `PUT /repos/{owner}/{repo}/contents/{path}
    """

    g = Github(config.access_token)
    repo = g.get_repo(config.repo)
    branch = config.branch or GithubObject.NotSet

    path = os.path.join(folder, filename)
    created = repo.create_file(
        path=path, content=content, message=comment, branch=branch
    )

    logger.info(
        f"File {path} was created in the {repo}, commit={created['commit'].sha}"
    )

    return created["content"]


def get_files_in_folder(config: Config, folder: str) -> List[ContentFile.ContentFile]:
    """
    Return the content of the folder

    :calls: `GET /repos/{owner}/{repo}/contents/{path}
    """
    g = Github(config.access_token)
    repo = g.get_repo(config.repo)
    branch = config.branch or GithubObject.NotSet

    files = [
        content
        for content in repo.get_contents(path=folder, ref=branch)
        if content.type == "file"
    ]

    return files