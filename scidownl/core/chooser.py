# -*- coding: utf-8 -*-
"""Implementations of ScihubUrlChooser"""
import random
from threading import RLock
from typing import Optional

from .base import ScihubUrlChooser
from ..db.entities import ScihubUrl
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

    def next(self) -> Optional[ScihubUrl]:
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

    def next(self) -> Optional[ScihubUrl]:
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


class AvailabilityFirstScihubUrlChooser(ScihubUrlChooser):
    """Availability-first chooser of scihub urls.
    A scihub url is considered as more available if it has a less failed rate
        failed_rate = (failed_times) / (success_times + failed_times + 0.01)
    The tail 0.01 is used to avoid divide by zero error if (success_times + failed_times) == 0.
    """
    __chooser_type__ = "availability_first"

    def __init__(self):
        self.service = ScihubUrlService()
        self.scihub_urls = self.service.get_all_urls()

        # Sort by availability.
        self.temp_zone = sorted(
            self.scihub_urls,
            key=lambda url: url.failed_times / (url.success_times + url.failed_times + 0.01)
        )

        self.cursor = 0
        self._lock = RLock()

    def next(self) -> Optional[ScihubUrl]:
        with self._lock:
            if self.cursor < 0 or self.cursor >= len(self.temp_zone):
                raise StopIteration
            selected_url = self.temp_zone[self.cursor]
            self.cursor += 1
            return selected_url

    def __len__(self):
        return len(self.temp_zone)


scihub_url_choosers = {
    "simple": SimpleScihubUrlChooser,
    "random": RandomScihubUrlChooser,
    "availability_first": AvailabilityFirstScihubUrlChooser
}
