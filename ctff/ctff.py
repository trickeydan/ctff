"""The main CTFF script."""
from __future__ import annotations

from pathlib import Path
from warnings import warn

from flask import Flask, current_app, render_template

from ctff.part import HTMLPart, MarkdownPart, Part

from .challenge_group import ChallengeGroup


class CTFF(Flask):
    """CTFFramework main class."""

    def __init__(
        self,
        secret_key: bytes,
        *,
        title: str = "CTF",
        template_folder: str | Path | None = None,
        parts: list[Part] | None = None,
        introduction_md: str | None = None,
        introduction_html: str | None = None,
    ) -> None:
        if template_folder is None:
            template_folder = Path(__file__).parent.resolve() / "templates"

        super().__init__(
            "CTFF",
            template_folder=template_folder,
        )

        self.secret_key = secret_key
        self.title = title
        self.parts = parts or []

        self._challenge_groups: list[ChallengeGroup] = []

        self.add_url_rule("/", view_func=self.index_view)

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

    def index_view(self) -> str:
        """Render the index view for the CTF."""
        return render_template(
            "index.html",
            challenge_groups=self._challenge_groups,
            ctff=current_app,
        )

    def register_challenge_group(self, challenge_group: ChallengeGroup) -> None:
        """Register a challenge group."""
        self._challenge_groups.append(challenge_group)

        group_slug = challenge_group.url_slug

        self.add_url_rule(
            f"/{group_slug}",
            f"{group_slug}_index",
            view_func=challenge_group.index_view,
        )

        for view in challenge_group.get_challenge_views():  # type: ignore
            challenge_slug = view.challenge.get_url_slug()
            self.add_url_rule(
                f"/{group_slug}/{challenge_slug}",
                view_func=view.as_view(f"{group_slug}_{challenge_slug}"),
            )

    def get_parts(self) -> list[Part]:
        parts = self.parts

        # Add deprecated parts
        if self._introduction_md is not None:
            parts.append(MarkdownPart(self._introduction_md))

        if self._introduction_html is not None:
            parts.append(HTMLPart(self._introduction_html))

        return parts
