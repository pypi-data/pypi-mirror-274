"""
.. include:: ../README.md
   :start-line: 1
   :end-before: Installation
"""

from .allspice import (
    AllSpice,
)
from .apiobject import (
    User,
    Organization,
    Team,
    Repository,
    Branch,
    Issue,
    Milestone,
    Commit,
    Comment,
    Content,
    DesignReview,
    Release,
)
from .exceptions import NotFoundException, AlreadyExistsException

__version__ = "3.1.0"

__all__ = [
    "AllSpice",
    "User",
    "Organization",
    "Team",
    "Repository",
    "Branch",
    "NotFoundException",
    "AlreadyExistsException",
    "Issue",
    "Milestone",
    "Commit",
    "Comment",
    "Content",
    "DesignReview",
    "Release",
]
