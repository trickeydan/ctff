"""The base challenge class."""
from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING

from slugify import slugify

from ctff.part import Part

if TYPE_CHECKING:
    from ctff.challenge_group import ChallengeGroup  # noqa: F401


class Challenge(metaclass=ABCMeta):
    """A challenge presents a problem to the competitor."""

    title = "Challenge"
    flag = "DEFAULT_FLAG"
    parts: list[Part] = []

    success_message = "You completed the challenge."
    failure_message = "Incorrect."

    def __init__(self, *, group: ChallengeGroup) -> None:
        self.group = group

    def get_failure_message(self) -> str:
        return self.failure_message

    def get_flag(self) -> str:
        return self.flag

    def get_success_message(self) -> str:
        return self.success_message

    def get_parts(self) -> list[Part]:
        return self.parts

    def get_title(self) -> str:
        return self.title

    def get_url_slug(self) -> str:
        """The URL slug."""
        return slugify(self.get_title())

    def verify_submission(self) -> bool:
        """Verify a submission."""
        return False
