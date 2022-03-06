# -*- encoding: utf-8 -*-
"""Core base abstract classes"""
from abc import ABC, abstractmethod
from os import PathLike
from typing import Union, Iterable, List, Optional

from ..db.entities import ScihubUrl


class BaseTask(ABC):
    """Abstract task with a `run` method."""
    def __init__(self):
        self.context = {}

    @abstractmethod
    def run(self):
        """Run the task."""
        raise NotImplementedError("Implement run method before calling it.")


class BaseTaskStep(ABC):
    """Abstract task step if a task.
    Every task step can access the task context.
    """
    def __init__(self, task: BaseTask):
        self.task = task


class BaseSource(ABC, dict):
    """Abstract source, which is a map that contains source item entries.
    """
    def __init__(self):
        super().__init__()
        self.type = 'base'


class BaseContent(ABC):
    """Abstract content.
    """
    def __init__(self, content=None):
        self.content = "" if content is None else content
        self.type = 'base'


class BaseCrawler(ABC):
    """Abstract crawler with a `crawl` method.
    Crawler is used to output the Content with the given Source.
    """
    def __init__(self, source: BaseSource):
        self.source = source

    @abstractmethod
    def crawl(self) -> BaseContent:
        """Crawl the source and returns the content of it.

        A typical crawling is accessing an url in the source, and
        returning the content with html string in it.
        """
        raise NotImplementedError("Implement crawl method before calling it.")


class BaseChecker(ABC):
    """Abstract checker with a `check` method.
    Checker is used to check the validity of Content.
    """
    def __init__(self, content: BaseContent):
        self.content = content

    @abstractmethod
    def check(self) -> bool:
        """Check and return whether the content is valid."""
        raise NotImplementedError("Implement check method before calling it.")


class BaseInformation(ABC, dict):
    """Abstract information, which is a map that contains information item entries.
    """
    def __init__(self):
        super().__init__()
        self.type = 'base'


class BaseExtractor(ABC):
    """Abstract extractor with an `extract` method.
    Extractor is used to extract information from the Content.
    """
    def __init__(self, content: BaseContent):
        self.content = content

    @abstractmethod
    def extract(self) -> BaseInformation:
        """Extract and return information from the content."""
        raise NotImplementedError("Implement extract method before calling it.")


class BaseDownloader(ABC):
    """Abstract downloader with a `download` method."""
    def __init__(self, information: BaseInformation):
        self.information = information

    @abstractmethod
    def download(self, out: str) -> str:
        """Download the information to local."""
        raise NotImplementedError("Implement download method before calling it.")


class DomainUpdater(ABC):
    """Abstract domain updater"""

    @abstractmethod
    def update_domains(self) -> Union[List, Iterable[str]]:
        """Returns a sequence of urls."""
        raise NotImplementedError("Implement update_domain method before calling it.")


class ScihubUrlChooser(ABC):
    """Abstract chooser for choosing scihub url."""

    __chooser_type__ = "base"

    @abstractmethod
    def next(self) -> Optional[ScihubUrl]:
        """Returns the next scihub url or None if reach the end."""
        raise NotImplementedError("Implement next method before calling it.")

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __len__(self):
        return 0
