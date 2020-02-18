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

    @classmethod
    def get_challenge(cls) -> Type[ChallengeT]:
        """Get the challenge to present."""
        raise NotImplementedError

    @classmethod
    def get_template_name(cls) -> str:
        """Get the name of the Jinja template."""
        return "challenge.html"

    def get(self) -> str:
        """Render and return a request."""
        challenge_class: Type[Challenge] = self.get_challenge()

        return render_template(
            self.get_template_name(),
            challenge=challenge_class(),
            challenge_group=challenge_class.group,
            ctff=current_app,
        )

    def post(self) -> Response:
        """Verify a submission."""
        challenge_class: Type[Challenge] = self.get_challenge()
        challenge = challenge_class()
        if challenge.verify_submission():
            flash(challenge.success_message, "success")
            flash(challenge.flag, "flag")
        else:
            flash(challenge.failure_message, "error")
        if challenge_class.group is None:
            raise RuntimeError
        else:
            return redirect(f"/{challenge_class.group.url_slug}/{challenge.get_url_slug()}")
