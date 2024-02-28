"""CTF Framework."""

from flask import request

from .challenge import Challenge
from .challenge_group import ChallengeGroup
from .ctff import CTFF

__all__ = [
    "__version__",
    "Challenge",
    "ChallengeGroup",
    "CTFF",
    "request",
]

__version__ = "0.3.3"
