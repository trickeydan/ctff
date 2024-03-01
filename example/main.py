from ctff import CTFF, Challenge, ChallengeGroup, request
from ctff.part import MarkdownPart, TextSubmissionPart

intro = """
This text is rendered as **markdown**.

You can also use the `introduction_html` argument to directly supply HTML source.
"""

app = CTFF(
    b"secret_key",
    title="My CTF",
    parts=[MarkdownPart(intro)],
)

challenge_group = ChallengeGroup("Basic Challenges", parts=[MarkdownPart(intro)])


@challenge_group.challenge
class MyChallenge(Challenge):
    title = "Super Easy"

    parts = [
        MarkdownPart(intro),
        TextSubmissionPart("example"),
    ]

    def get_flag(self) -> str:
        if "application/json" in request.accept_mimetypes:
            return "flag{somethingElse}"
        else:
            return "flag{exampleFlag}"

    def verify_submission(self) -> bool:
        return request.form["example"] == "bees"


app.register_challenge_group(challenge_group)

if __name__ == "__main__":
    app.run(debug=True)
