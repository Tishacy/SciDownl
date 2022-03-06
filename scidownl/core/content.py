# -*- coding: utf-8 -*-
"""Content implementations."""

from .base import BaseContent


class HtmlContent(BaseContent):
    """Content stores html string."""
    def __init__(self, html: str = None):
        super().__init__(html)
        self.type = 'html'

    def __repr__(self):
        return f"HtmlContent[html = {self.content}]"

    def __len__(self):
        return len(self.content)


class JsonContent(BaseContent):
    """Content stores JSON object."""
    def __init__(self, json: dict = None):
        super().__init__(json)
        self.type = 'json'

    def __repr__(self):
        return f"JsonContent[json = {self.content}]"

    def __len__(self):
        return len(self.content)
