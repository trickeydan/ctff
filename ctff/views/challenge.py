"""Challenge View."""
from typing import TypeVar, Type

from flask.templating import render_template
from flask.views import View

from ctff.challenge import Challenge

ChallengeT = TypeVar("ChallengeT", bound=Challenge)


class ChallengeView(View):
    """Renders and processes a challenge."""

    @classmethod
    def get_challenge(cls) -> Type[ChallengeT]:
        """Get the challenge to present."""
        raise NotImplementedError

    @classmethod
    def get_template_name(cls) -> str:
        """Get the name of the Jinja template."""
        return "challenge.html"

    def dispatch_request(self, **context):
        """Render and return a request."""
        return render_template(self.get_template_name(), **context)
