#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Optional, Tuple, Union, Iterable
from sys import argv

from anytree import (
    AbstractStyle,
    AsciiStyle,
    ChildResolverError,
    NodeMixin,
    RenderTree,
    Resolver,
)
import click


class ClickTreeParam(click.ParamType):
    """Click Tree Parameter.

    This pseudo-parameter will generate and render a tree of the click Command
    it is decorated with.

    Example Usage:
    @click.command(name="foobar)
    @click.option(
        "--tree",
        is_flag=True,
        type=ClickTreeParam(scoped=True, ignore_names=["smn-run"]),
        help="Enable tree display.",
    )
    def cli(tree: Optional[bool]) -> None:
        ...

    If `--tree` is provided, the command will then render the tree and exit.
    Otherwise, it will continue execution as normal.

    Args:
        scoped: bool. If True, sys.argv will be used to "scope" the rendered
            tree down to the current invocation, only showing the tree from
            the provided command onward.
        ignore_names: Optional[Iterable[str]]. List of command/group names to
            filter out during tree display.
        style: Optional[AbstractStyle]. Override the anytree style used to render
            the tree. Defaults to AsciiStyle. Style reference:
            https://anytree.readthedocs.io/en/stable/api/anytree.render.html
    """

    name = "click_tree"

    def __init__(
        self,
        scoped: bool = False,
        ignore_names: Optional[Iterable[str]] = None,
        style: Optional[AbstractStyle] = None,
    ) -> None:
        self.scoped = scoped
        self.ignore_names = ignore_names
        self.style = style

    def convert(
        self,
        # Original click.ParamType.convert signature, not changing.
        # pyre-ignore[2]: Parameter `value` must have a type other than `Any`.
        value: Any,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> None:
        if not isinstance(value, bool):
            click.secho(
                "click.Option should be defined with is_flag=True when using ClickTreeParam"
            )
            raise click.exceptions.Exit(1)
        elif not ctx:
            click.secho("No click.Context found, cannot resolve root command")
            raise click.exceptions.Exit(1)
        elif value:
            # Tree parameter specified by user, render.
            tree = get_tree(ctx.find_root().command, argv if self.scoped else None)
            click.secho(tree.render(style=self.style, ignore_names=self.ignore_names))
            raise click.exceptions.Exit(0)
        else:
            # Not rendering tree, return.
            return None


class ClickNode(NodeMixin):
    """A single Node in the Click command tree.

    Args:
        name: str. Name of the command.
        description: Optional[str]. Description of the command, if any.
        default_command: bool. Whether or not this command is a "default" command.
            This only applies to Groups using click-contrib/click-default-group.
            Defaults to False.
        parent: Optional[ClickNode]. Parent ClickNode.
        children: Optional[Tuple[ClickNode, ...]]. Child ClickNode(s).
    """

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        default_command: bool = False,
        parent: Optional[ClickNode] = None,
        children: Optional[Tuple[ClickNode, ...]] = None,
    ) -> None:
        super().__init__()

        self.name = name
        self.description = description
        self.default_command = default_command

        self.parent = parent
        if children:
            self.children: Tuple[ClickNode, ...] = children

    @classmethod
    def from_click_obj(
        cls,
        click_obj: Union[click.Command, click.Group],
        name: str,
        default_command: bool = False,
        parent: Optional[ClickNode] = None,
    ) -> ClickNode:
        """Generate a ClickNode tree from a given Click Command or Group.

        This will retrieve all relevant metadata about a given click object and
        create a ClickNode for it. If click_obj is a Group, it will recursively
        add all Commands/Groups under it as well.

        Args:
            click_obj: Union[click.Command, click.Group]. Click object to generate
                ClickNode tree for.
            command_name: Optional[str]. Optional name override, if not provided the
                `name` property of the provided click_obj will be used.
            parent: Optional[ClickNode]. Parent ClickNode of this Node, supplied
                recursively during command enumeration.

        Returns:
            click_node: ClickNode. Node representing the full tree of the provided
                click object.
        """

        node = ClickNode(
            name=name,
            default_command=default_command,
            parent=parent,
        )

        if isinstance(click_obj, click.Group):
            description = click_obj.short_help

            # Attempt to retrieve default_cmd_name, defaulting to None
            # if this is just a normal click.Group and not a DefaultGroup.
            default_cmd_name = getattr(click_obj, "default_cmd_name", None)

            # Add all the subcommands of this group as children recursively.
            node.children = tuple(
                cls.from_click_obj(command, name, default_cmd_name == name, node)
                for name, command in click_obj.commands.items()
            )
        else:
            description = click_obj.help

        if description:
            # Retrieve first non-empty line of the description.
            description = next((line for line in description.split("\n") if line), "")

            if len(description) > 80:
                description = f"{description[:77]}..."
            else:
                description = description[:80]

            node.description = description

        return node

    def render(
        self,
        style: Optional[AbstractStyle] = None,
        ignore_names: Optional[Iterable[str]] = None,
    ) -> str:
        """Render and return the ClickNode tree.

        Args:
            style: Optional[AbstractStyle]. Anytree "style" to use for rendering
                tree. Defaults to AsciiStyle().
            ignore_names: Optional[Iterable[str]]. Collection of command names
                that will be skipped if found during tree rendering.

        Returns:
            rendered_tree: str. Rendered ClickNode tree.
        """

        if not style:
            style = AsciiStyle()

        if not ignore_names:
            ignore_names = tuple()

        render_str = ""
        for row in RenderTree(self, style):
            node = row.node

            if node.name in ignore_names:
                continue

            # Add a suffix which shows truncated help if there is help defined.
            help_str = f" - {node.description}" if node.description else ""

            default_str = " (*)" if node.default_command else ""

            # Default, with help
            # toggle (*) - toggle state
            # Not default, with help
            # state - get state
            # Not default, no help
            # on
            render_str += f"{row.pre}{node.name}{default_str}{help_str}\n"

        return render_str


def _get_command_path(
    root: Union[click.Command, click.Group], argv: Iterable[str]
) -> str:
    """Resolve the tree "path" for a given command invocation.

    Given a sys.argv like:
    ['/the/path/to/my/script',
    '--tree',
    'living',
    'lights']

    This will attempt to resolve each argument against the supplied root, adding
    it's name to the path if found, and updating the root if the resolved click
    object is also a group. (In this example /root_command/living/lights).

    Args:
        root: Union[click.Command, click.Group]. Root click object to resolve
            path with.
        argv: Iterable[str]. Arguments, usually from sys.argv, representing the
            current click invocation.

    Returns:
        command_path: str. Resolved command path.
    """

    path = f"/{root.name}"
    if not isinstance(root, click.Group):
        # The root is a command, just return the path to the root node.
        return path

    node = root
    for arg in argv:
        # Attempt to resolve the arg as a command in the current Group.
        if resolved_obj := node.commands.get(arg, None):
            # If it was resolved, add the name to the path.
            path += f"/{resolved_obj.name}"

            if isinstance(resolved_obj, click.Group):
                # If this is also a group, update the current node to the
                # resolved group, so that the next argument(s) can be resolved
                # against it.
                node = resolved_obj

    # Return the full path.
    return path


def get_tree(
    root: Union[click.Command, click.Group], argv: Optional[Iterable[str]] = None
) -> ClickNode:
    """Generate and return a ClickNode tree for a given click root object and argv.

    If argv are provided, it will also "scope" the tree down to the invoked
    command, only rendering it from that point on.

    Args:
        root: Union[click.Command, click.Group]. Root click object to generate
            tree from.
        argv: Iterable[str]. Arguments, usually from sys.argv, representing the
            current click invocation, used for scoping.

    Returns:
        click_tree: Generated ClickNode tree from the root object, optionally
            scoped for the current invocation.
    """

    name = root.name
    if name is not None:
        tree = ClickNode.from_click_obj(root, name)
    else:
        tree = ClickNode.from_click_obj(root, "")

    if not argv:
        # No scoping, just return entire tree.
        return tree

    command_path = _get_command_path(root, argv)
    if command_path == "/":
        # Root command, return the entire tree.
        return tree
    else:
        # Resolve the scoped path.
        return Resolver("name").get(tree, command_path)
