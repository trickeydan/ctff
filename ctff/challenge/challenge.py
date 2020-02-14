"""The base challenge class."""

from abc import ABCMeta, abstractmethod


class Challenge(metaclass=ABCMeta):
    """A challenge presents a problem to the competitor."""

    @property
    @abstractmethod
    def title(cls) -> str:
        """The title of the challenge."""
        raise NotImplementedError

    @classmethod
    def get_url_slug(cls) -> str:
        """The URL slug."""
        return cls.title
