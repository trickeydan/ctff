from ctff import Challenge, ChallengeGroup, CTFF

intro = """
This text is rendered as **markdown**.

You can also use the `introduction_html` argument to directly supply HTML source.
"""

app = CTFF(
    title="My CTF",
    introduction_md=intro,
)


class MyChallenge(Challenge):

    title = "Super Easy"


challenge_group = ChallengeGroup("Basic Challenges", introduction_md=intro)

challenge_group.add_challenge(MyChallenge)

app.register_challenge_group(challenge_group)

if __name__ == "__main__":
    app.run(debug=True)
