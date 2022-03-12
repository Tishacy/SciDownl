# -*- encoding: utf-8 -*-
"""Downloader implementation."""
import os
import sys

import requests

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
            proxies = self.task.context.get('proxies', {}) if self.task is not None else {}
            res = requests.get(url, stream=True, proxies=proxies)
            total_length = res.headers.get('content-length')

            with open(out, "wb") as f:
                if total_length is None:
                    # no content length header
                    f.write(res.content)
                else:
                    download_length = 0
                    total_length = int(total_length)
                    bar_width = 50
                    for data in res.iter_content(chunk_size=4096):
                        download_length += len(data)
                        f.write(data)
                        done_width = int(bar_width * download_length / total_length)
                        perc = int(100 * download_length / total_length)
                        sys.stdout.write("\r%3d%% [%s%s] %s/%s"
                                         % (perc, '=' * done_width,
                                            ' ' * (bar_width - done_width),
                                            download_length, total_length))
                        sys.stdout.flush()
                    sys.stdout.write('\n')
                    sys.stdout.flush()
            _, filename = os.path.split(out)
            logger.info(f"↓ Successfully download the url to: {out}")

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

