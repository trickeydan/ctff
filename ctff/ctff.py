"""The main CTFF script."""
from importlib import resources

from flask import Flask

from .challenge_group import ChallengeGroup


class CTFF(Flask):
    """CTFFramework main class."""

    def __init__(self, **kwargs) -> None:

        with resources.path("ctff", "templates") as path:
            template_folder = str(path.absolute())

        kwargs["template_folder"] = template_folder

        super().__init__("CTFF", **kwargs)

    def register_challenge_group(self, challenge_group: ChallengeGroup) -> None:
        """Register a challenge group."""
        for view in challenge_group.get_views():
            challenge_class = view.get_challenge()
            self.add_url_rule(f"/{challenge_group.url_slug}/{challenge_class.url_slug()}", view_func=view.as_view(challenge_class.url_slug()))
