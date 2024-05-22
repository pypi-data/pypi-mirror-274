# mkdocs statblock plugin

This mkdocs plugin scans your files for `statblock` code blocks and renders them
as statblocks. The statblock templates are defined with jinja templates, which
allows for great flexibility and thus supports virtually any system - all you
need is data in yaml format, and the template.

## Installation

```sh
pip install mkdocs-statblock-plugin
```

### Requirements

* Python >= 3.6
* MkDocs >= 1.6.0

## Configuration

| Option             | Description                                                                               | Required | Default |
| ------------------ | ----------------------------------------------------------------------------------------- | :------: | :-----: |
| `templates`        | The directory to scan for statblock templates. Relative to project root.                  |    x     |         |
| `default_template` | The default template to use if none is specified in a statblock. Relative to `templates`. |          |         |
| `bestiary`         | The directory to scan for statblocks. Relative to project root.                           |          |   `/`   |

Add the following lines to your `mkdocs.yml`:

```yaml
plugins:
  - statblocks:
      templates: docs/_statblocks/templates/
      default_template: template.html
```

> Tip: Put the templates in your docs folder so the page is automatically
> reloaded when using `mkdocs serve`.

The `templates` configuration tells the plugin which directory to scan for
statblock templates. A statblock can then reference the template by its filename
(including the file extension, e.g. `dnd5e.html`).

````md
```statblock
monster: My D&D 5e Monster
template: dnd5e.html
```
````

If the `template` option in a statblock is omitted, the plugin will use the
`default_template` instead.

By default the plugin scans all files in your projct root for statblocks (files
with `.yaml` extension). You can override the root folder of your bestiary by
adding the following configuration:

```yaml
plugins:
  - statblocks:
      - bestiary: bestiary/
```

The bestiary folder is relative to the `docs_dir`. For example:

```
- docs/
  - bestiary/
    - goblin.yaml
    - orc.yaml
  - my cool file.md
mkdocs.yml
```

You can get most official Pathfinder 1e statblocks from [Pathfinder1
Statblocks](https://github.com/johannes-z/pathfinder1-statblocks), including
templates and basic styling.

## Usage

The most basic usage is saving a statblock as `.yaml`-file under the bestiary
folder, and referencing it in your markdown file like this:

````md
# My Monster

```statblock
monster: My Monster
```
````

This will search for a `my-monster.yaml` file in your bestiary folder, extract
its contents and render the statblock.

If you want to override some values, you can do so by adding them to the code
block. Check the existing `.yaml`-file for how specify the values. The order of
the properties does not matter - it will always override the base monster with
your custom definition.

````md
# My Monster

```statblock
monster: My Monster
Name: My Custom Monster
CR: 20
Melee: null # erase the base monster's Melee definition
```
````

Of course you can design a monster from scratch, by omitting the `monster`
property.


## Roadmap

* [x] Custom templates and a way to specify which template to use in statblocks
* [ ] Performance fixes - only include statblock files that are referenced.

## License
MIT License © 2024-PRESENT Johannes Zwirchmayr
