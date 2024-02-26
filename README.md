# CTFF - CTF Framework

A Framework for building CTFs.

CTFF can be used to define Capture The Flag (CTF) challenges in a very minimal
amount of code, and render an interface for competitors to view and attempt
challenges. Building a mini web-interface seems to be a thing that we frequently
do when building a CTF and this framework aims to reduce that effort to near-zero.

CTFF is built on top of [Flask](https://flask.palletsprojects.com/) and supplements it's functionality.
All of the usual Flask features and functionality are still available.

## CTF Structure

The framework currently assumes that CTFs consist of a series of challenges, which are grouped
together. The groups might be levels, or categories of challenges, the framework leaves it up to the author.

Each challenge consists of a number of "parts", one of which will usually be a submission. A challenge can only have one submission pathway, but multiple solutions or inputs if desired.

```python
@challenge_group.challenge
class MyChallenge(Challenge):
    title = "My Challenge"
    flag = "flag{ZzZzZzZ}"

    def __init__(self) -> None:
        self.parts = [
            MarkdownPart("What lives in a hive and goes zzzz?"),
            TextSubmissionPart("example"),
        ]

    def verify_submission(self) -> bool:
        return request.form["example"] == "bees"
```

## Contributions

This project is released under the MIT Licence. For more information, please see LICENSE.
