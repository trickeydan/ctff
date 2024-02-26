"""The main CTFF script."""
from __future__ import annotations

from importlib import resources

import mistune
from flask import Flask, current_app, render_template

from .challenge_group import ChallengeGroup


class CTFF(Flask):
    """CTFFramework main class."""

    def __init__(
        self,
        secret_key: bytes,
        *,
        title: str = "CTF",
        template_folder: str | None = None,
        introduction_md: str | None = None,
        introduction_html: str = "",
    ) -> None:
        if template_folder is None:
            with resources.path("ctff", "templates") as path:
                template_folder = str(path.absolute())

        super().__init__(
            "CTFF",
            template_folder=template_folder,
        )

        self.secret_key = secret_key
        self._title = title
        self._introduction_md = introduction_md
        self._introduction_html = introduction_html
        self._challenge_groups: list[ChallengeGroup] = []

        self.add_url_rule("/", view_func=self.index_view)

    def index_view(self) -> str:
        """Render the index view for the CTF."""
        return render_template(
            "index.html",
            challenge_groups=self._challenge_groups,
            ctff=current_app,
        )

    @property
    def challenge_groups(self) -> list[ChallengeGroup]:
        """The challenge groups."""
        return self._challenge_groups

    @property
    def introduction_html(self) -> str:
        """
        The HTML for the CTF introduction.

        If introduction_md is set, this will be rendered from it.
        """
        if self._introduction_md is None:
            return self._introduction_html
        else:
            return mistune.markdown(self._introduction_md)

    @property
    def title(self) -> str:
        """The title of the CTF."""
        return self._title

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
