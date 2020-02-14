from ctff import Challenge, ChallengeGroup, CTFF


class MyChallenge(Challenge):

    title = "a"


app = CTFF()

challenge_group = ChallengeGroup("Basic")

challenge_group.add_challenge(MyChallenge)

app.register_challenge_group(challenge_group)

if __name__ == "__main__":
    app.run()
