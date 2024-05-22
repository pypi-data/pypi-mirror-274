import os
import glob
import mkdocs
from .statblock_handler import StatBlockHandler
from mkdocs.structure.files import Files as MkDocsFiles
from mkdocs.config.defaults import MkDocsConfig
from pathlib import Path
from collections import defaultdict

TemplatesType = defaultdict[str, Path]
BestiaryType = defaultdict[str, Path]


class StatBlockPluginConfig(mkdocs.config.base.Config):
    templates = mkdocs.config.config_options.Type(str)
    default_template = mkdocs.config.config_options.Type(str)
    bestiary = mkdocs.config.config_options.Type(str, default="/")


class StatBlockPlugin(mkdocs.plugins.BasePlugin[StatBlockPluginConfig]):
    def __init__(self):
        self.templates: TemplatesType | None = None
        self.bestiary: BestiaryType | None = None

    def on_config(self, config):
        self.templatesPath = os.path.join(os.getcwd(), self.config.templates)
        self.bestiaryPath = os.path.join(os.getcwd(), self.config.bestiary)

        if self.bestiary is None:
            self.bestiary = defaultdict(list)
            files = glob.iglob(os.path.join(self.bestiaryPath, "*.yaml"))
            for filename in files:
                filepath = os.path.join(self.bestiaryPath, filename)
                file = Path(filepath)
                self.bestiary[file.name] = filepath

        return config

    def on_page_markdown(self, markdown, page, config, files):
        handler = StatBlockHandler(
            self.templates,
            self.templatesPath,
            self.config.default_template,
            self.bestiary,
        )
        return handler.process_statblocks(markdown)

    def on_files(self, files: MkDocsFiles, *, config: MkDocsConfig) -> MkDocsFiles:
        """Initialize the filename lookup dict if it hasn't already been initialized"""

        if self.templates is None:
            self.templates = defaultdict(list)
            for file in files:
                filepath = Path(file.abs_src_path)
                if not str(filepath).startswith(self.templatesPath):
                    continue
                self.templates[filepath.name] = filepath

        return files
