import os
import mkdocs
from .statblock_handler import StatBlockHandler
from mkdocs.structure.files import Files as MkDocsFiles
from mkdocs.config.defaults import MkDocsConfig
from pathlib import Path
from collections import defaultdict

BestiaryType = defaultdict[str, list[Path]]


class StatBlockPluginConfig(mkdocs.config.base.Config):
    bestiary = mkdocs.config.config_options.Type(str, default="/")


class StatBlockPlugin(mkdocs.plugins.BasePlugin[StatBlockPluginConfig]):
    def __init__(self):
        self.bestiary: BestiaryType | None = None

    def on_config(self, config):
        self.bestiaryPath = os.path.join(config.docs_dir, self.config.bestiary)
        return config

    def on_page_markdown(self, markdown, page, config, files):
        handler = StatBlockHandler(self.bestiary)
        return handler.process_statblocks(markdown)

    def on_files(self, files: MkDocsFiles, *, config: MkDocsConfig) -> MkDocsFiles:
        """Initialize the filename lookup dict if it hasn't already been initialized"""

        if self.bestiary is None:
            self.bestiary = defaultdict(list)
            for file in files:
                filepath = Path(file.abs_src_path)
                if not str(filepath).startswith(self.bestiaryPath):
                    continue
                self.bestiary[filepath.name] = filepath
        return files
