#!/usr/bin/env python3
from inspect import cleandoc
from typing import Any, Optional

from click_tree import __name__ as _BASE, ClickTreeParam, ClickNode, get_tree

from anytree.exporter import DictExporter
import click
from click.testing import CliRunner
from testslide import TestCase


class ClickTreeTests(TestCase):
    def setUp(self) -> None:
        @click.group("tree_test", short_help="test the click tree")
        @click.option(
            "--tree",
            is_flag=True,
            type=ClickTreeParam(scoped=True, ignore_names=["smn-run"]),
            help="Enable tree display.",
        )
        @click.pass_context
        def tree_test_click(click_ctx: click.Context, tree: Optional[bool]) -> None:
            pass

        @tree_test_click.command("root_command", help="a root command")
        def root_command_click() -> None:
            pass

        @tree_test_click.group("root_group", short_help="a root group")
        def root_group_click() -> None:
            pass

        @root_group_click.group(
            "sub_group",
            short_help="a sub group",
        )
        def sub_group_click() -> None:
            pass

        @sub_group_click.command(
            "default_command", help="default command of the sub group"
        )
        def default_command_click() -> None:
            pass

        # This "simulates" ClickTree's interactions with DefaultGroup without
        # requiring it to be present in this repo.
        sub_group_click.default_cmd_name = "default_command"

        @sub_group_click.command(
            "other_command", help="another command of the sub group"
        )
        def other_command_click() -> None:
            pass

        sub_group = ClickNode(name="sub_group", description="a sub group")
        sub_group.children = (
            ClickNode(
                name="default_command",
                description="default command of the sub group",
                default_command=True,
                parent=sub_group,
            ),
            ClickNode(
                name="other_command",
                description="another command of the sub group",
                parent=sub_group,
            ),
        )

        root = ClickNode(name="tree_test", description="test the click tree")

        root_group = ClickNode(
            name="root_group", description="a root group", parent=root
        )
        root_group.children = (sub_group,)

        root.children = (
            ClickNode(name="root_command", description="a root command", parent=root),
            root_group,
        )

        self.click_root = tree_test_click
        self.expected_tree = root

        self.exporter = DictExporter()
        self.runner = CliRunner()

    def test_click_tree(self) -> None:
        tree = get_tree(self.click_root)

        self.assertEqual(
            self.exporter.export(tree), self.exporter.export(self.expected_tree)
        )

    def test_click_tree_scoped(self) -> None:
        argv = ["/some/fake/path", "--tree", "root_group", "--some-arg", "sub_group"]
        tree = get_tree(self.click_root, argv)

        root_group = next(
            child for child in self.expected_tree.children if child.name == "root_group"
        )
        sub_group = next(
            child for child in root_group.children if child.name == "sub_group"
        )

        self.assertEqual(self.exporter.export(tree), self.exporter.export(sub_group))

    def test_click_tree_render(self) -> None:
        expected_stdout = cleandoc(
            """\
            tree_test - test the click tree
            |-- root_command - a root command
            +-- root_group - a root group
                +-- sub_group - a sub group
                    |-- default_command (*) - default command of the sub group
                    +-- other_command - another command of the sub group
            """
        )

        result = self.runner.invoke(self.click_root, "--tree")
        self.assertEqual(result.stdout.rstrip(), expected_stdout)

    def test_click_tree_param(self) -> None:
        # Ensuring that the get_tree method was called in response to
        # the --tree arg is the only thing needed here. Deeper tests are
        # handled above.
        self.mock_callable(_BASE, "get_tree").to_return_value(
            self.expected_tree
        ).and_assert_called_once()

        result = self.runner.invoke(self.click_root, "--tree")
        self.assertEqual(result.exit_code, 0)

    def test_click_tree_param_not_called(self) -> None:
        self.mock_callable(_BASE, "get_tree").to_return_value(
            self.expected_tree
        ).and_assert_called_exactly(0)

        result = self.runner.invoke(self.click_root)
        self.assertEqual(result.exit_code, 0)

    def test_click_tree_param_not_bool(self) -> None:
        @click.group("tree_test", short_help="test the click tree")
        @click.option(
            "--tree",
            type=ClickTreeParam(),
            help="Enable tree display.",
        )
        @click.pass_context
        def tree_test_click(click_ctx: click.Context, tree: Optional[bool]) -> None:
            pass

        result = self.runner.invoke(tree_test_click, "--tree=bad")
        self.assertEqual(result.exit_code, 1)
