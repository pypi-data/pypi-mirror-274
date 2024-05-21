import os
import sys
import re
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import File


logger = get_plugin_logger(__name__)


link_pattern = re.compile(r'<(.+.md)>')


class AutoLinkTitlePluginConfig(Config):
    param = config_options.Type(str, default='')


class AutoLinkTitlePlugin(BasePlugin[AutoLinkTitlePluginConfig]):
    _page_titles = None

    def __init__(self):
        logger.info("AutoLinkTitlePlugin __init__")
        
    def on_page_markdown(self, markdown, page, config, files):
        if self._page_titles is None:
            logger.info("on_page_markdown: _page_titles init")
            self._page_titles = {}
            for file in files:
                if isinstance(file, File) and file.src_path.endswith('.md'):
                    if file.page.title is None:
                        file.page.read_source(config)
                        file.page.render(config, files)

                    self._page_titles[file.src_uri] = file.page.title
        
        _page_titles = self._page_titles

        def _replacer(match):
            link_filepath = match.group(1)
            link_filepath_normalized = os.path.normpath(os.path.join(os.path.dirname(page.file.src_uri), link_filepath))
            if link_filepath_normalized in _page_titles:
                return f'[{_page_titles[link_filepath_normalized]}]({link_filepath})'
            
            return match.group(0)

        return re.sub(link_pattern, _replacer, markdown)
