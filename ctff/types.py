"""Common type variables."""
from typing import TypeVar

from .challenge.challenge import Challenge
from .views.challenge import ChallengeView

ChallengeT = TypeVar("ChallengeT", bound=Challenge)
ChallengeViewT = TypeVar("ChallengeViewT", bound=ChallengeView)