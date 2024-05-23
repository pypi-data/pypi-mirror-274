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

## Example

### Goblin

_Example Goblin as provided by [Pathfinder1
Statblocks](https://github.com/johannes-z/pathfinder1-statblocks). Description omitted for brevity._

<table>
<tr>
<td>

````yaml
Name: Goblin
CR: 1/3
XP: '135'
Race: Goblin
Class: warrior 1
Alignment: NE
Size: Small
Type: humanoid
SubType: (goblinoid)
Init: '6'
Senses:
  - darkvision 60 ft.
  - Perception -1
AC: 16, touch 13, flat-footed 14
AC_Mods: (+2 armor, +2 Dex, +1 shield, +1 size)
HP: '6'
HD: (1d10+1)
Saves: Fort +3, Ref +2, Will -1
Fort: '3'
Ref: '2'
Will: '-1'
Speed: 30 ft.
Melee:
  - short sword +2 (1d4/19-20)
Ranged:
  - short bow +4 (1d4/x3)
Space: 5 ft.
Reach: 5 ft.
AbilityScores:
  - 11
  - 15
  - 12
  - 10
  - 9
  - 6
BaseAtk: '1'
CMB: '0'
CMD: '12'
Feats:
  - Improved Initiative
Skills:
  - Ride +10
  - Stealth +10
  - Swim +4
RacialMods: +4 Ride, +4 Stealth
Languages:
  - Goblin
Environment: temperate forest and plains (usually coastal regions)
Organization: >-
  gang (4-9), warband (10-16 with goblin dog mounts), or tribe (17+ plus 100%
  noncombatants; 1 sergeant of 3rd level per 20 adults; 1 or 2 lieutenants of
  4th or 5th level; 1 leader of 6th-8th level; and 10-40 goblin dogs, wolves, or
  worgs)
Treasure: >-
  NPC gear (leather armor, light wooden shield, short sword, short bow with 20
  arrows, other treasure)
Description_Visual: >-
  This creature stands barely three feet tall, its scrawny, humanoid body
  dwarfed by its wide, ungainly head.
Source: PFRPG Bestiary
IsTemplate: '0'
CharacterFlag: '1'
CompanionFlag: '0'
Fly: '0'
Climb: '0'
Burrow: '0'
Swim: '0'
Land: '1'
AgeCategory: adult
DontUseRacialHD: '1'
CompanionFamiliarLink: 'NULL'
LinkText: Goblin
id: '214'
UniqueMonster: '0'
MR: '0'
Mythic: '0'
MT: '0'
````

</td>
<td>

> The template for this statblock is fully customizable. Here the Pathfinder 1e
> template is used.

![Example Goblin](_assets/example-goblin.png)

</td>
</tr>
</table>

## License
MIT License © 2024-PRESENT Johannes Zwirchmayr
