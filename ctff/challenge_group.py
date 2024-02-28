"""A group of challenges."""
from __future__ import annotations

from collections.abc import Collection
from typing import Iterator, TypeVar
from warnings import warn

from flask import current_app, render_template
from slugify import slugify

from .challenge import Challenge, ChallengeView
from .part import HTMLPart, MarkdownPart, Part

ChallengeViewT = TypeVar("ChallengeViewT", bound=ChallengeView)


class ChallengeGroup(Collection):
    """A group of challenges."""

    def __init__(
        self,
        name: str,
        *,
        parts: list[Part] | None = None,
        introduction_md: str | None = None,
        introduction_html: str | None = None,
    ) -> None:
        self.name = name
        self.parts = parts or []
        self._challenges: list[Challenge] = []

        self._introduction_md = introduction_md
        self._introduction_html = introduction_html

        # Warn about deprecated args
        if introduction_md is not None:
            warn(
                "introduction_md is deprecated and will be removed in ctff v0.5.0",
                DeprecationWarning,
                stacklevel=2,
            )

        if introduction_html is not None:
            warn(
                "introduction_html is deprecated and will be removed in ctff v0.5.0",
                DeprecationWarning,
                stacklevel=2,
            )

    @property
    def url_slug(self) -> str:
        """Get a url slug."""
        return slugify(self.name)

    def __len__(self) -> int:
        return len(self._challenges)

    def __iter__(self) -> Iterator[Challenge]:
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

    def add_challenge(self, challenge_type: type[Challenge]) -> None:
        """Add a challenge."""
        challenge = challenge_type(group=self)
        self._challenges.append(challenge)

    def challenge(self, cls: type[Challenge]) -> type[Challenge]:
        """Register a challenge."""
        self.add_challenge(cls)
        return cls

    def get_challenge_views(self) -> list[type[ChallengeViewT]]:
        """Get the challenge views that we need to add."""
        return [challenge.get_view() for challenge in self._challenges]

    def get_parts(self) -> list[Part]:
        parts = self.parts

        # Add deprecated parts
        if self._introduction_md is not None:
            parts.append(MarkdownPart(self._introduction_md))

        if self._introduction_html is not None:
            parts.append(HTMLPart(self._introduction_html))

        return parts
