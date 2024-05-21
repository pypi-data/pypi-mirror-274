# Click Tree

`click_tree` is a utility library for the [click](https://click.palletsprojects.com) 
CLI framework which generates a tree of any click CLI:

```bash
smn --tree home
home - home automation (hass-cli)
|-- all - all rooms
|   +-- lights - toggle all lights
|-- kitchen - kitchen
|   +-- lights
|       |-- set (*) - set brightness level (0-100)
|       |-- level - get brightness level (0-100)
|       |-- toggle - toggle state
|       |-- state - get state
|       |-- on - turn on
|       +-- off - turn off
|-- living - living room
|   |-- lights
|   |   |-- set (*) - set brightness level (0-100)
|   |   |-- level - get brightness level (0-100)
|   |   |-- toggle - toggle state
|   |   |-- state - get state
|   |   |-- on - turn on
|   |   +-- off - turn off
|   |-- fan
|   |   |-- toggle (*) - toggle state
|   |   |-- state - get state
|   |   |-- on - turn on
|   |   +-- off - turn off
|   |-- humidifier
|   |   |-- toggle (*) - toggle state
|   |   |-- state - get state
|   |   |-- on - turn on
|   |   +-- off - turn off
|   |-- temp - temperature (f)
|   +-- humid - relative humidity (%)
```

This library uses [anytree](https://anytree.readthedocs.io/en/stable/index.html) 
for constructing and rendering the tree.

The original inspiration for this tree implementation was based off of the 
[click-command-tree](https://github.com/whwright/click-command-tree) library 
created by Harrison Wright.

# Usage

## Parameter

The click tree can be implemented as a click Parameter type, ClickTreeParam, 
which should be added to the root of the CLI:

```python
from typing import Optional

import click
from click_tree import ClickTreeParam

@click.group(name="smn")
@click.option(
    "--tree",
    is_flag=True,
    type=ClickTreeParam(scoped=True),
    help="Enable tree display.",
)
def cli(tree: Optional[bool]) -> None:
    pass
```

Passing the `--tree` option will then cause the CLI to display the tree and exit. 
With the `scoped=True` option, the tree will only display from the user invoked 
command onwards. For example, `smn --tree`, would render the entire tree, while 
`smn --tree home` would only render all subcommands and groups from `home` onwards.

## Manual

Manual implementation is possible with the `get_tree` command, which takes a 
"root" click object, either a Command or a Group, as well as optionally a set 
of `argv` to use for scoping the generated tree:

```python
from typing import Optional
from sys import argv

import click
from click_tree import get_tree

@click.group(name="smn")
def cli() -> None:
    pass

@cli.command(name="tree")
@click.pass_context
def cli_tree(ctx: click.Context) -> None:
    tree = get_tree(ctx.find_root().command, argv)

    click.secho(tree.render())
```

# Configuration

ClickTreeParam has several options for customizing behavior during tree render:

```
scoped: bool. If True, sys.argv will be used to "scope" the rendered
    tree down to the current invocation, only showing the tree from
    the provided command onward.
ignore_names: Optional[Iterable[str]]. List of command/group names to
    filter out during tree display.
style: Optional[AbstractStyle]. Override the anytree style used to render
    the tree. Defaults to AsciiStyle. Style reference:
    https://anytree.readthedocs.io/en/stable/api/anytree.render.html
```

For manual implementation, the `ignore_names` and `style` parameters can be 
provided to `tree.render()`.

# Development

Install in development mode:
```bash
pip3 install -e '.[dev]'
```

## Type Checking

Ensure no type errors are present with [pyre](https://github.com/facebook/pyre-check):

```bash
pyre check              
ƛ No type errors found
```

## Formatting

Format code with the [black](https://github.com/psf/black) formatter:

```bash
black click_tree
All done! ✨ 🍰 ✨
```

## Testing

Ensure tests pass with [TestSlide](https://github.com/facebook/TestSlide):

```bash
cd test
testslide test_click_tree.py     
test_click_tree.ClickTreeTests
  test_click_tree
  test_click_tree_param
  test_click_tree_param_not_bool
  test_click_tree_param_not_called
  test_click_tree_render
  test_click_tree_scoped
                                                               --_ |""---__
Executed 6 examples in 0.1s:                                |'.|  ||  .    """|
  Successful: 6                                             | ||  || /|\""-.  |
  Failed: 0                                                 | ||  ||  |    |  |
  Skipped: 0                                                | ||  ||  |   \|/ |
  Not executed: 0                                           |."|  ||  --"" '__|
https://testslide.readthedocs.io/
```
