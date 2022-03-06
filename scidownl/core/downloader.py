# -*- encoding: utf-8 -*-
"""Downloader implementation."""
from os import PathLike
from typing import Union

import wget

from .base import BaseDownloader, BaseTask, BaseTaskStep
from .information import UrlInformation
from ..log import get_logger
from ..exception import DownloadException
from ..db.service import ScihubUrlService

logger = get_logger()


class UrlDownloader(BaseDownloader, BaseTaskStep):
    """Downloader of url."""

    def __init__(self, information: UrlInformation, task: BaseTask = None):
        BaseDownloader.__init__(self, information)
        BaseTaskStep.__init__(self, task)
        self.information = information
        self.task = task
        self.service = ScihubUrlService()
        if self.task is not None:
            self.task.context['status'] = 'downloading'

    def download(self, out: str) -> str:
        """Download a url to out"""
        try:
            url = self.information.get_url()
            filename = wget.download(url, out)
            print()
            logger.info(f"↓ Successfully download the url to: {filename}")

            if self.task is not None:
                self.task.context['out'] = out
                self.task.context['filename'] = filename
        except Exception as e:
            if self.task is not None:
                self.task.context['status'] = 'downloading_failed'
                self.task.context['error'] = e
                scihub_url = self.task.context.get('referer', None)
                self.service.increment_failed_times(scihub_url)
            raise DownloadException(f"Error occurs when downloading {e}")
        return filename

