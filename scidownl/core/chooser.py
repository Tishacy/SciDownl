# -*- coding: utf-8 -*-
"""Implementations of ScihubUrlChooser"""
import random
from threading import RLock
from typing import Optional

from .base import ScihubUrlChooser
from ..db.service import ScihubUrlService


class SimpleScihubUrlChooser(ScihubUrlChooser):
    """Simple chooser of scihub urls, which would choose
    scihub urls based on the order in the database table.
    """
    __chooser_type__ = "simple"

    def __init__(self):
        self.service = ScihubUrlService()
        self.scihub_urls = self.service.get_all_urls()
        self.cursor = 0
        self._lock = RLock()

    def next(self) -> Optional[str]:
        with self._lock:
            if self.cursor < 0 or self.cursor >= len(self.scihub_urls):
                raise StopIteration
            selected_url = self.scihub_urls[self.cursor]
            self.cursor += 1
            return selected_url

    def __len__(self):
        return len(self.scihub_urls)


class RandomScihubUrlChooser(ScihubUrlChooser):
    """Random chooser of scihub urls, which would choose
    scihub urls randomly, and one url won't be chosen twice.
    """
    __chooser_type__ = "random"

    def __init__(self):
        self.service = ScihubUrlService()
        self.scihub_urls = self.service.get_all_urls()
        self.temp_zone = [url for url in self.scihub_urls]
        self.cursor = 0
        self._lock = RLock()

    def next(self) -> Optional[str]:
        with self._lock:
            if len(self.temp_zone) == 0:
                raise StopIteration

            # Randomly choose a scihub url.
            selected_url = random.choice(self.temp_zone)
            # Exclude the selected url in later selection.
            self.temp_zone = [url for url in self.temp_zone if url != selected_url]
            return selected_url

    def __len__(self):
        return len(self.temp_zone)


scihub_url_choosers = {
    "simple": SimpleScihubUrlChooser,
    "random": RandomScihubUrlChooser,
    # "availability_first": AvailabilityFirstScihubUrlChooser
}
