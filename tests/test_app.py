from flask.testing import FlaskClient

from ctff import CTFF


class TestCTFFIndex:
    def test_get(self, example_app: CTFF, client: FlaskClient) -> None:
        resp = client.get("/")

        assert resp.status_code == 200
        assert example_app.introduction_html in resp.text
        assert "This CTF contains 1 categories of challenge." in resp.text
        assert '<a href="/basic-challenges">Basic Challenges</a>' in resp.text


class TestCTFFChallengeGroup:
    def test_get(self, example_app: CTFF, client: FlaskClient) -> None:
        resp = client.get("/basic-challenges")

        challenge_group = example_app._challenge_groups[0]

        assert resp.status_code == 200
        assert challenge_group.introduction_html in resp.text
        assert f"<h1>{challenge_group.name}</h1>" in resp.text
        assert '<a href="/basic-challenges/super-easy">Super Easy</a>' in resp.text


class TestCTFFChallenge:
    def test_get(self, example_app: CTFF, client: FlaskClient) -> None:
        resp = client.get("/basic-challenges/super-easy")

        challenge_group = example_app._challenge_groups[0]
        challenge = challenge_group._challenges[0]

        assert resp.status_code == 200
        assert f"<h1>{challenge.title}</h1>" in resp.text

    def test_post(self, example_app: CTFF, client: FlaskClient) -> None:
        resp = client.post("/basic-challenges/super-easy", data={"example": "bees"})

        challenge_group = example_app._challenge_groups[0]
        challenge = challenge_group._challenges[0]

        assert resp.status_code == 200
        assert f"<h1>{challenge.title}</h1>" in resp.text
        assert "You completed the challenge." in resp.text
        assert "flag{exampleFlag}" in resp.text

    def test_post_incorrect(self, example_app: CTFF, client: FlaskClient) -> None:
        resp = client.post("/basic-challenges/super-easy", data={"example": "wasps"})

        challenge_group = example_app._challenge_groups[0]
        challenge = challenge_group._challenges[0]

        assert resp.status_code == 200
        assert f"<h1>{challenge.title}</h1>" in resp.text
        assert "Incorrect." in resp.text
