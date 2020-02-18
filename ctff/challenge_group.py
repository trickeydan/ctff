"""A group of challenges."""
from collections.abc import Collection
from typing import Iterator, List, Optional, Type, TypeVar

import mistune
from flask import current_app, render_template
from slugify import slugify

from .challenge import Challenge
from .challenge_view import ChallengeView

ChallengeT = TypeVar("ChallengeT", bound=Challenge)
ChallengeViewT = TypeVar("ChallengeViewT", bound=ChallengeView)


class ChallengeGroup(Collection):
    """A group of challenges."""

    def __init__(
            self,
            name: str,
            *,
            introduction_md: Optional[str] = None,
            introduction_html: str = "",
    ):
        self.name = name
        self._introduction_md = introduction_md
        self._introduction_html = introduction_html

        self._challenges: List[Type[ChallengeT]] = []  # type: ignore

    @property
    def url_slug(self) -> str:
        """Get a url slug."""
        return slugify(self.name)

    @property
    def introduction_html(self) -> str:
        """
        The HTML for the Challenge Group introduction.

        If introduction_md is set, this will be rendered from it.
        """
        if self._introduction_md is None:
            return self._introduction_html
        else:
            return mistune.markdown(self._introduction_md)

    def __len__(self) -> int:
        return len(self._challenges)

    def __iter__(self) -> Iterator[Type[ChallengeT]]:
        return iter(self._challenges)

    def __contains__(self, __x: object) -> bool:
        return __x in self._challenges

    def index_view(self) -> str:
        """Render the page for the challenge group."""
        return render_template(
            "challenge_group.html",
            challenge_group=self,
            ctff=current_app,
        )

    def add_challenge(self, challenge: Type[Challenge]) -> None:
        """Add a challenge."""
        challenge.group = self
        self._challenges.append(challenge)

    def challenge(self, cls: Type[Challenge]) -> Type[Challenge]:
        """Register a challenge."""
        self.add_challenge(cls)
        return cls

    def get_challenge_views(self) -> List[Type[ChallengeViewT]]:
        """Get the challenge views that we need to add."""
        views: List[Type[ChallengeViewT]] = []

        for chal in self._challenges:

            class SpecificChallengeView(ChallengeView):

                challenge = chal

            views.append(SpecificChallengeView)  # type: ignore
        return views
