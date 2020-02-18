"""The base challenge class."""

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, List, Optional, cast

from slugify import slugify

from ctff.part import Part

if TYPE_CHECKING:
    from ctff.challenge_group import ChallengeGroup  # noqa: F401


class Challenge(metaclass=ABCMeta):
    """A challenge presents a problem to the competitor."""

    group: Optional['ChallengeGroup'] = None
    parts: List[Part] = []
    success_message: str = "You completed the challenge."
    failure_message: str = "Incorrect."
    flag: str = "DEFAULT_FLAG"

    @property
    @abstractmethod
    def title(cls) -> str:
        """The title of the challenge."""
        raise NotImplementedError

    @classmethod
    def get_url_slug(cls) -> str:
        """The URL slug."""
        return slugify(cast(str, cls.title))

    def verify_submission(self) -> bool:
        """Verify a submission."""
        return False
