"""A group of challenges."""
from collections.abc import Collection
from typing import Iterator, List, Type, TypeVar

from flask import current_app, render_template
from slugify import slugify

from .challenge import Challenge
from .challenge_view import ChallengeView

ChallengeT = TypeVar("ChallengeT", bound=Challenge)
ChallengeViewT = TypeVar("ChallengeViewT", bound=ChallengeView)


class ChallengeGroup(Collection):
    """A group of challenges."""

    def __init__(self, name: str):
        self.name = name
        self._challenges: List[Type[ChallengeT]] = []  # type: ignore

    @property
    def url_slug(self) -> str:
        """Get a url slug."""
        return slugify(self.name)

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

    def get_challenge_views(self) -> List[Type[ChallengeViewT]]:
        """Get the challenge views that we need to add."""
        views: List[Type[ChallengeViewT]] = []

        for chal in self._challenges:
            class SpecificChallengeView(ChallengeView):

                @classmethod
                def get_challenge(cls) -> Type[ChallengeT]:
                    return chal

            views.append(SpecificChallengeView)  # type: ignore
        return views
