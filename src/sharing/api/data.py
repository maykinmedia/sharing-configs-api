from dataclasses import dataclass


@dataclass
class FileData:
    slug: str
    folder: str
    filename: str
    content: bytes = None
