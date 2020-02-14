"""Challenge View."""
from typing import Any, Type, TypeVar

from flask.helpers import current_app
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

    def dispatch_request(self, *args: Any, **kwargs: Any) -> Any:
        """Render and return a request."""
        challenge_class: Type[Challenge] = self.get_challenge()

        return render_template(
            self.get_template_name(),
            challenge=challenge_class(),
            challenge_group=challenge_class.group,
            ctff=current_app,
        )
