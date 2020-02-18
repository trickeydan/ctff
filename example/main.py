from ctff import Challenge, ChallengeGroup, CTFF
from ctff.part import MarkdownPart

from flask import request

intro = """
This text is rendered as **markdown**.

You can also use the `introduction_html` argument to directly supply HTML source.
"""

app = CTFF(
    b"secret_key",
    title="My CTF",
    introduction_md=intro,
)

challenge_group = ChallengeGroup("Basic Challenges", introduction_md=intro)


@challenge_group.challenge
class MyChallenge(Challenge):

    title = "Super Easy"
    parts = [
        MarkdownPart(intro)
    ]

    def verify_submission(self) -> bool:
        return request.json == {}


app.register_challenge_group(challenge_group)

if __name__ == "__main__":
    app.run(debug=True)
