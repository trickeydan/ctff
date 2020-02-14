"""The base challenge class."""

from abc import ABCMeta, abstractmethod


class Challenge(metaclass=ABCMeta):
    """A challenge presents a problem to the competitor."""

    @classmethod
    @abstractmethod
    def title(cls) -> str:
        """The title of the challenge."""
        raise NotImplementedError

    @classmethod
    def url_slug(cls) -> str:
        """The URL slug."""
        return cls.title
