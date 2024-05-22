import yaml
import os
import re
from jinja2 import Environment, FileSystemLoader


def kebabize(string):
    if string:
        parts = re.findall(
            r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+", string
        )
        return "-".join(map(str.lower, parts))
    else:
        return ""


def modifierFilter(input):
    try:
        input = int(input)
        return f"+{input}" if input >= 0 else input
    except ValueError:
        return input


def testFilter(input, label, default=""):
    if not input:
        return default
    if label:
        return f"<b>{label}</b> {input}"
    return input


class StatBlockHandler:
    def __init__(self, templates, templates_path, default_template, bestiary):
        self.templates = templates
        self.default_template = default_template
        self.bestiary = bestiary
        self.template_env = Environment(loader=FileSystemLoader(templates_path))
        self.template_env.filters["modifier"] = modifierFilter
        self.template_env.filters["testFilter"] = testFilter

    def process_statblocks(self, markdown_content):
        statblock_pattern = r"```statblock\n(.*?)```"

        statblocks = re.findall(statblock_pattern, markdown_content, re.DOTALL)

        processed_content = markdown_content
        for statblock in statblocks:
            statblock_data = self.extendMonster(yaml.safe_load(statblock))

            template = self.template_env.get_template(
                statblock_data.get("template")
                if statblock_data.get("template")
                else self.default_template
            )

            rendered_statblock = template.render(statblock_data)
            processed_content = processed_content.replace(
                f"```statblock\n{statblock}```", rendered_statblock
            )

        return processed_content

    def extendMonster(self, data):
        """Extends the monster statblock with the base monster data if it exists in the bestiary."""
        if "monster" not in data:
            return data
        monster_name = data["monster"]
        kebab_name = kebabize(monster_name)
        baseMonsterFilePath = self.bestiary[kebab_name + ".yaml"]
        if os.path.exists(baseMonsterFilePath):
            with open(baseMonsterFilePath, "r") as f:
                monster_data = yaml.safe_load(f)
            data = {**monster_data, **data}
        return data
