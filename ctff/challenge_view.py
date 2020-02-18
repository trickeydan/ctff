"""Challenge View."""
from typing import Type, TypeVar

from flask import current_app, flash, redirect
from flask.templating import render_template
from flask.views import MethodView
from werkzeug.wrappers import Response

from ctff.challenge import Challenge

ChallengeT = TypeVar("ChallengeT", bound=Challenge)


class ChallengeView(MethodView):
    """Renders and processes a challenge."""

    challenge: Type[Challenge]

    @classmethod
    def get_template_name(cls) -> str:
        """Get the name of the Jinja template."""
        return "challenge.html"

    def get(self) -> str:
        """Render and return a request."""
        return render_template(
            self.get_template_name(),
            challenge=self.challenge(),
            challenge_group=self.challenge.group,
            ctff=current_app,
        )

    def post(self) -> Response:
        """Verify a submission."""
        challenge = self.challenge()
        if challenge.verify_submission():
            flash(challenge.success_message, "success")
            flash(challenge.flag, "flag")
        else:
            flash(challenge.failure_message, "danger")
        if self.challenge.group is None:
            raise RuntimeError
        else:
            return redirect(
                f"/{self.challenge.group.url_slug}/{challenge.get_url_slug()}",
            )
