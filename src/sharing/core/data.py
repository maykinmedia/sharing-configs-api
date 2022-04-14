""" data class helpers to work with file storage backends"""
from dataclasses import dataclass, field
from typing import List


@dataclass()
class Folder:
    name: str
    children: List["Folder"] = field(default_factory=list)
