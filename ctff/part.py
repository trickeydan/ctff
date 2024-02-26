"""A part of a challenge."""
from abc import ABCMeta, abstractmethod

import mistune
from flask import render_template


class Part(metaclass=ABCMeta):
    """A part of a challenge."""

    @abstractmethod
    def render(self) -> str:
        """Render as html."""
        raise NotImplementedError


class TemplatePart(Part, metaclass=ABCMeta):
    """A part that renders as a template."""

    template_name: str

    def render(self) -> str:
        """Render as html."""
        return render_template(self.template_name, part=self)


class TextSubmissionPart(TemplatePart):
    """Submit a text form."""

    template_name = "parts/text_submission.html"

    def __init__(self, name: str) -> None:
        self.name = name


class MarkdownPart(Part):
    """A part that renders some markdown."""

    def __init__(self, content: str) -> None:
        self.content = content

    def render(self) -> str:
        """Render as html."""
        return mistune.markdown(self.content)
