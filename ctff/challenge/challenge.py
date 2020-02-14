"""The base challenge class."""

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Optional, cast

import mistune
from slugify import slugify

if TYPE_CHECKING:
    from ctff.challenge_group import ChallengeGroup  # noqa: F401


class Challenge(metaclass=ABCMeta):
    """A challenge presents a problem to the competitor."""

    group: Optional['ChallengeGroup'] = None

    @property
    @abstractmethod
    def title(cls) -> str:
        """The title of the challenge."""
        raise NotImplementedError

    @classmethod
    def get_url_slug(cls) -> str:
        """The URL slug."""
        return slugify(cast(str, cls.title))

    @property
    def introduction_html(self) -> str:
        """
        The HTML for the Challenge introduction.

        If introduction_md is set, this will be rendered from it.
        """
        if self.introduction_md is None:
            return ""
        else:
            return mistune.markdown(self.introduction_md)

    @property
    def introduction_md(self) -> Optional[str]:
        """Markdown for the Challenge."""
        return None
