"""Challenge View."""
from __future__ import annotations

from logging import Logger
from typing import TYPE_CHECKING

from flask import current_app, flash
from flask.templating import render_template
from flask.views import MethodView

if TYPE_CHECKING:
    from ctff.challenge import Challenge

LOGGER = Logger(__name__)


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
            ctff=current_app,
        )

    def post(self) -> str:
        """Verify a submission."""
        if self.challenge.verify_submission():
            flash(self.challenge.get_success_message(), "success")
            flash(self.challenge.get_flag(), "flag")
            LOGGER.error(f"{self.challenge.get_title()} has been solved.")
        else:
            flash(self.challenge.get_failure_message(), "danger")

        return self.get()
