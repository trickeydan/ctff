"""Challenge View."""
from __future__ import annotations

from logging import Logger
from typing import TypeVar

from flask import current_app, flash
from flask.templating import render_template
from flask.views import MethodView

from ctff.challenge import Challenge

LOGGER = Logger(__name__)

ChallengeT = TypeVar("ChallengeT", bound=Challenge)


class ChallengeView(MethodView):
    """Renders and processes a challenge."""

    challenge: Challenge

    def get_template_name(self) -> str:
        """Get the name of the Jinja template."""
        return "challenge.html"

    def get(self) -> str:
        """Render and return a request."""
        return render_template(
            self.get_template_name(),
            challenge=self.challenge,
            challenge_group=self.challenge.group,
            ctff=current_app,
        )

    def post(self) -> str:
        """Verify a submission."""
        challenge = self.challenge

        if challenge.verify_submission():
            flash(challenge.success_message, "success")
            flash(challenge.flag, "flag")
            LOGGER.error(f"{challenge.title} has been solved.")
        else:
            flash(challenge.failure_message, "danger")

        return self.get()
