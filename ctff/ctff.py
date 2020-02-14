"""The main CTFF script."""
from importlib import resources
from typing import Any, List

from flask import Flask, render_template, current_app

from .challenge_group import ChallengeGroup


class CTFF(Flask):
    """CTFFramework main class."""

    def __init__(self, **kwargs: Any) -> None:

        with resources.path("ctff", "templates") as path:
            template_folder = str(path.absolute())

        kwargs["template_folder"] = template_folder

        if "title" in kwargs.keys():
            self.title = kwargs.pop("title")
        else:
            self.title = "CTF"

        super().__init__("CTFF", **kwargs)

        self._challenge_groups: List[ChallengeGroup] = []

        self.before_first_request(self._setup)

    def _setup(self) -> None:
        self.add_url_rule("/", view_func=self.index_view)

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
            challenge_class = view.get_challenge()
            challenge_slug = challenge_class.get_url_slug()
            self.add_url_rule(
                f"/{group_slug}/{challenge_slug}",
                view_func=view.as_view(f"{group_slug}_{challenge_slug}"),
            )
