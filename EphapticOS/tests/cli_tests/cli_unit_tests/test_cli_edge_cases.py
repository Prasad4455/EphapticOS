"""
Tests for CLI edge cases and error scenarios with proper mocking.
"""

import argparse
import asyncio
import os
import sys
from unittest.mock import ANY, AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

import EphapticOS
from EphapticOS.cli.commands.add_command import AddCommand
from EphapticOS.cli.commands.Ephaptify_command import EphaptifyCommand
from EphapticOS.cli.commands.config_command import ConfigCommand
from EphapticOS.cli.commands.delete_command import DeleteCommand
from EphapticOS.cli.commands.search_command import SearchCommand
from EphapticOS.cli.exceptions import CliCommandException
from EphapticOS.modules.data.methods.get_deletion_counts import DeletionCountsPreview
from EphapticOS.modules.engine.operations.setup import setup


# Mock asyncio.run to properly handle coroutines
def _mock_run(coro):
    # Create an event loop and run the coroutine
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _mock_user():
    u = MagicMock()
    u.id = uuid4()
    return u


_RESOLVE_USER_PATCH = "EphapticOS.cli.user_resolution.resolve_cli_user"


class TestAddCommandEdgeCases:
    """Test edge cases for AddCommand"""

    @patch(_RESOLVE_USER_PATCH, new_callable=lambda: AsyncMock(return_value=_mock_user()))
    @patch("EphapticOS.cli.commands.add_command.asyncio.run", side_effect=_mock_run)
    def test_add_empty_data_list(self, mock_asyncio_run, _mock_resolve):
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.add = AsyncMock()

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = AddCommand()
            args = argparse.Namespace(data=[], dataset_name="test_dataset")
            command.execute(args)

        mock_asyncio_run.assert_called_once()
        assert asyncio.iscoroutine(mock_asyncio_run.call_args[0][0])
        mock_EphapticOS.add.assert_awaited_once_with(data=[], dataset_name="test_dataset", user=ANY)

    @patch("EphapticOS.cli.commands.add_command.asyncio.run")
    def test_add_asyncio_run_exception(self, mock_asyncio_run):
        """Test add command when asyncio.run itself fails"""
        command = AddCommand()
        args = argparse.Namespace(data=["test.txt"], dataset_name="test_dataset")

        mock_asyncio_run.side_effect = RuntimeError("Event loop error")

        with pytest.raises(CliCommandException):
            command.execute(args)

    def test_add_special_characters_in_data(self):
        """Test add command with special characters in file paths"""
        command = AddCommand()

        # Create parser to test argument parsing with special characters
        parser = argparse.ArgumentParser()
        command.configure_parser(parser)

        # Test parsing with special characters
        special_paths = [
            "file with spaces.txt",
            "file-with-dashes.txt",
            "file_with_underscores.txt",
            "file.with.dots.txt",
        ]

        args = parser.parse_args(special_paths + ["--dataset-name", "test"])
        assert args.data == special_paths
        assert args.dataset_name == "test"


class TestSearchCommandEdgeCases:
    """Test edge cases for SearchCommand"""

    @patch(_RESOLVE_USER_PATCH, new_callable=lambda: AsyncMock(return_value=_mock_user()))
    @patch("EphapticOS.cli.commands.search_command.asyncio.run", side_effect=_mock_run)
    def test_search_empty_results(self, mock_asyncio_run, _mock_resolve):
        """Test search command with empty results"""
        # Mock the EphapticOS module and SearchType
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.search = AsyncMock(return_value=[])
        mock_search_type = MagicMock()
        mock_search_type.__getitem__.return_value = "GRAPH_COMPLETION"

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = SearchCommand()
            args = argparse.Namespace(
                query_text="nonexistent query",
                query_type="GRAPH_COMPLETION",
                datasets=None,
                top_k=10,
                system_prompt=None,
                output_format="pretty",
            )

            # Should handle empty results gracefully
            command.execute(args)

        mock_asyncio_run.return_value = []
        mock_asyncio_run.assert_called_once()
        assert asyncio.iscoroutine(mock_asyncio_run.call_args[0][0])
        mock_EphapticOS.search.assert_awaited_once_with(
            query_text="nonexistent query",
            query_type=ANY,
            user=ANY,
            datasets=None,
            top_k=10,
            system_prompt_path="answer_simple_question.txt",
            session_id=ANY,
        )
        # verify the enum’s name separately
        called_enum = mock_EphapticOS.search.await_args.kwargs["query_type"]
        assert called_enum.name == "GRAPH_COMPLETION"

    @patch(_RESOLVE_USER_PATCH, new_callable=lambda: AsyncMock(return_value=_mock_user()))
    @patch("EphapticOS.cli.commands.search_command.asyncio.run", side_effect=_mock_run)
    def test_search_very_large_top_k(self, mock_asyncio_run, _mock_resolve):
        """Test search command with very large top-k value"""
        # Mock the EphapticOS module and SearchType
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.search = AsyncMock(return_value=["result1"])
        mock_search_type = MagicMock()
        mock_search_type.__getitem__.return_value = "CHUNKS"

        mock_asyncio_run.return_value = ["result1"]

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = SearchCommand()
            args = argparse.Namespace(
                query_text="test query",
                query_type="CHUNKS",
                datasets=None,
                top_k=999999,  # Very large value
                system_prompt=None,
                output_format="json",
            )

            command.execute(args)

        mock_asyncio_run.assert_called_once()
        assert asyncio.iscoroutine(mock_asyncio_run.call_args[0][0])
        mock_EphapticOS.search.assert_awaited_once_with(
            query_text="test query",
            query_type=ANY,
            user=ANY,
            datasets=None,
            top_k=999999,
            system_prompt_path="answer_simple_question.txt",
            session_id=ANY,
        )
        # verify the enum’s name separately
        called_enum = mock_EphapticOS.search.await_args.kwargs["query_type"]
        assert called_enum.name == "CHUNKS"

    @patch("builtins.__import__")
    def test_search_invalid_search_type_enum(self, mock_import):
        """Test search command with invalid SearchType enum conversion"""
        # Mock SearchType to raise KeyError
        mock_search_type = MagicMock()
        mock_search_type.__getitem__.side_effect = KeyError("INVALID_TYPE")

        def mock_import_func(name, fromlist=None, *args, **kwargs):
            if name == "EphapticOS.modules.search.types":
                module = MagicMock()
                module.SearchType = mock_search_type
                return module
            return MagicMock()

        mock_import.side_effect = mock_import_func

        command = SearchCommand()
        args = argparse.Namespace(
            query_text="test query",
            query_type="INVALID_TYPE",  # This would fail enum conversion
            datasets=None,
            top_k=10,
            system_prompt=None,
            output_format="pretty",
        )

        with pytest.raises(CliCommandException):
            command.execute(args)

    def test_search_unicode_query(self):
        """Test search command with unicode characters in query"""
        command = SearchCommand()
        parser = argparse.ArgumentParser()
        command.configure_parser(parser)

        unicode_query = "测试查询 🔍 émojis and spéciál chars"
        args = parser.parse_args([unicode_query])
        assert args.query_text == unicode_query

    @patch(_RESOLVE_USER_PATCH, new_callable=lambda: AsyncMock(return_value=_mock_user()))
    @patch("EphapticOS.cli.commands.search_command.asyncio.run", side_effect=_mock_run)
    def test_search_results_with_none_values(self, mock_asyncio_run, _mock_resolve):
        """Test search command when results contain None values"""
        # Mock the EphapticOS module and SearchType
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.search = AsyncMock(return_value=[None, "valid result", None])
        mock_search_type = MagicMock()
        mock_search_type.__getitem__.return_value = "CHUNKS"

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = SearchCommand()
            args = argparse.Namespace(
                query_text="test query",
                query_type="CHUNKS",
                datasets=None,
                top_k=10,
                system_prompt=None,
                output_format="pretty",
            )

            # Should handle None values gracefully
            command.execute(args)

        mock_asyncio_run.assert_called_once()
        assert asyncio.iscoroutine(mock_asyncio_run.call_args[0][0])
        mock_EphapticOS.search.assert_awaited_once_with(
            query_text="test query",
            query_type=ANY,
            user=ANY,
            datasets=None,
            top_k=10,
            system_prompt_path="answer_simple_question.txt",
            session_id=ANY,
        )
        # verify the enum’s name separately
        called_enum = mock_EphapticOS.search.await_args.kwargs["query_type"]
        assert called_enum.name == "CHUNKS"


class TestEphaptifyCommandEdgeCases:
    """Test edge cases for EphaptifyCommand"""

    @patch(_RESOLVE_USER_PATCH, new_callable=lambda: AsyncMock(return_value=_mock_user()))
    @patch("EphapticOS.cli.commands.Ephaptify_command.asyncio.run", side_effect=_mock_run)
    def test_Ephaptify_invalid_chunk_size(self, mock_asyncio_run, _mock_resolve):
        """Test Ephaptify command with invalid chunk size"""
        # Mock the EphapticOS module
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.Ephaptify = AsyncMock()

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = EphaptifyCommand()
            args = argparse.Namespace(
                datasets=None,
                chunk_size=-100,  # Invalid negative chunk size
                ontology_file=None,
                chunker="TextChunker",
                background=False,
                verbose=False,
            )

            # Should pass the invalid value to Ephaptify and let it handle the validation
            command.execute(args)

        mock_asyncio_run.assert_called_once()
        assert asyncio.iscoroutine(mock_asyncio_run.call_args[0][0])
        from EphapticOS.modules.chunking.TextChunker import TextChunker

        mock_EphapticOS.Ephaptify.assert_awaited_once_with(
            datasets=None,
            user=ANY,
            chunk_size=-100,
            config=None,
            chunker=TextChunker,
            run_in_background=False,
            chunks_per_batch=None,
            dry_run=False,
        )

    @patch("EphapticOS.cli.commands.Ephaptify_command.asyncio.run", side_effect=_mock_run)
    def test_Ephaptify_nonexistent_ontology_file(self, mock_asyncio_run):
        """Test Ephaptify command fails fast on a nonexistent ontology file"""
        # Mock the EphapticOS module
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.Ephaptify = AsyncMock()

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = EphaptifyCommand()
            args = argparse.Namespace(
                datasets=None,
                chunk_size=None,
                ontology_file="/nonexistent/path/ontology.owl",
                chunker="TextChunker",
                background=False,
                verbose=False,
            )

            with pytest.raises(CliCommandException, match="Ontology file not found"):
                command.execute(args)

        mock_EphapticOS.Ephaptify.assert_not_awaited()

    @patch("EphapticOS.cli.commands.Ephaptify_command.asyncio.run")
    def test_Ephaptify_langchain_chunker_import_error(self, mock_asyncio_run):
        """Test Ephaptify command when LangchainChunker import fails"""
        # Mock the EphapticOS module
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.Ephaptify = AsyncMock()

        def mock_import_func(name, fromlist=None, *args, **kwargs):
            if name == "EphapticOS":
                return mock_EphapticOS
            elif (
                name == "EphapticOS.modules.chunking.LangchainChunker"
                and fromlist
                and "LangchainChunker" in fromlist
            ):
                raise ImportError("LangchainChunker not available")
            elif (
                name == "EphapticOS.modules.chunking.TextChunker"
                and fromlist
                and "TextChunker" in fromlist
            ):
                module = MagicMock()
                module.TextChunker = MagicMock()
                return module
            return MagicMock()

        with (
            patch("builtins.__import__", side_effect=mock_import_func),
            patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}),
        ):
            command = EphaptifyCommand()
            args = argparse.Namespace(
                datasets=None,
                chunk_size=None,
                ontology_file=None,
                chunker="LangchainChunker",
                background=False,
                verbose=True,
            )

            # Should fall back to TextChunker and show warning
            command.execute(args)

        mock_asyncio_run.assert_called_once()
        assert asyncio.iscoroutine(mock_asyncio_run.call_args[0][0])

    @patch(_RESOLVE_USER_PATCH, new_callable=lambda: AsyncMock(return_value=_mock_user()))
    @patch("EphapticOS.cli.commands.Ephaptify_command.asyncio.run", side_effect=_mock_run)
    def test_Ephaptify_empty_datasets_list(self, mock_asyncio_run, _mock_resolve):
        """Test Ephaptify command with an empty datasets list"""
        # Mock the EphapticOS module
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.Ephaptify = AsyncMock()

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = EphaptifyCommand()
            args = argparse.Namespace(
                datasets=[],
                chunk_size=None,
                ontology_file=None,
                chunker="TextChunker",
                background=False,
                verbose=False,
            )

            command.execute(args)

        mock_asyncio_run.assert_called_once()
        assert asyncio.iscoroutine(mock_asyncio_run.call_args[0][0])
        from EphapticOS.modules.chunking.TextChunker import TextChunker

        mock_EphapticOS.Ephaptify.assert_awaited_once_with(
            datasets=None,
            user=ANY,
            chunk_size=None,
            config=None,
            chunker=TextChunker,
            run_in_background=False,
            chunks_per_batch=None,
            dry_run=False,
        )


class TestDeleteCommandEdgeCases:
    """Test edge cases for DeleteCommand"""

    @patch(_RESOLVE_USER_PATCH, new_callable=lambda: AsyncMock(return_value=_mock_user()))
    @patch("EphapticOS.cli.commands.delete_command.asyncio.run", side_effect=_mock_run)
    @patch("EphapticOS.cli.commands.delete_command.EphapticOS_datasets")
    def test_delete_all_with_user_id(self, datasets_mock, async_run_mock, _mock_resolve):
        """Test delete command with --all and --force"""
        data_directory_path = os.path.join(
            os.path.dirname(__file__), ".data_storage/test_cli_commands"
        )
        EphapticOS_directory_path = os.path.join(
            os.path.dirname(__file__), ".EphapticOS_system/test_cli_commands"
        )

        EphapticOS.config.data_root_directory(data_directory_path)
        EphapticOS.config.system_root_directory(EphapticOS_directory_path)

        asyncio.run(EphapticOS.prune.prune_data())
        asyncio.run(EphapticOS.prune.prune_system(metadata=True))

        asyncio.run(setup())

        delete_all_mock = AsyncMock()
        datasets_mock.delete_all = delete_all_mock

        command = DeleteCommand()
        args = argparse.Namespace(
            dataset_name=None,
            all=True,
            force=True,
        )

        command.execute(args)

        delete_all_mock.assert_awaited_once_with(user=ANY)

        asyncio.run(EphapticOS.prune.prune_data())
        asyncio.run(EphapticOS.prune.prune_system(metadata=True))

    @patch("EphapticOS.cli.commands.delete_command.get_deletion_counts")
    @patch("EphapticOS.cli.commands.delete_command.fmt.confirm")
    def test_delete_confirmation_keyboard_interrupt(self, mock_confirm, mock_get_deletion_counts):
        """Test delete command when user interrupts confirmation"""
        mock_get_deletion_counts = AsyncMock()
        mock_get_deletion_counts.return_value = DeletionCountsPreview()

        command = DeleteCommand()
        args = argparse.Namespace(dataset_name="test_dataset")

        mock_confirm.side_effect = KeyboardInterrupt()

        # Should handle KeyboardInterrupt gracefully
        with pytest.raises(KeyboardInterrupt):
            command.execute(args)

    @patch("EphapticOS.cli.commands.delete_command.asyncio.run")
    def test_delete_async_exception_handling(self, mock_asyncio_run):
        """Test delete command async exception handling"""
        command = DeleteCommand()
        args = argparse.Namespace(dataset_name="test_dataset", user_id=None, all=False, force=True)

        # Mock asyncio.run to raise exception directly
        mock_asyncio_run.side_effect = ValueError("Database connection failed")

        with pytest.raises(CliCommandException):
            command.execute(args)

    def test_delete_special_characters_in_dataset_name(self):
        """Test delete command with special characters in dataset name"""
        command = DeleteCommand()
        parser = argparse.ArgumentParser()
        command.configure_parser(parser)

        special_names = [
            "dataset with spaces",
            "dataset-with-dashes",
            "dataset_with_underscores",
            "dataset.with.dots",
            "dataset/with/slashes",
        ]

        for name in special_names:
            args = parser.parse_args(["--dataset-name", name])
            assert args.dataset_name == name


class TestConfigCommandEdgeCases:
    """Test edge cases for ConfigCommand"""

    def test_config_no_subcommand_specified(self):
        """Test config command when no subcommand is specified"""
        command = ConfigCommand()
        parser = argparse.ArgumentParser()
        command.configure_parser(parser)

        # Parse with no subcommand - should set config_action to None
        args = parser.parse_args([])
        assert not hasattr(args, "config_action") or args.config_action is None

    @patch("builtins.__import__")
    def test_config_get_nonexistent_key(self, mock_import):
        """Test config get with nonexistent key"""
        # Mock config.get to raise exception for nonexistent key
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.config.get = MagicMock(side_effect=KeyError("Key not found"))
        mock_import.return_value = mock_EphapticOS

        command = ConfigCommand()
        args = argparse.Namespace(config_action="get", key="nonexistent_key")

        # Should handle the exception gracefully
        command.execute(args)
        mock_EphapticOS.config.get.assert_called_once_with("nonexistent_key", reveal_secrets=False)

    @patch("builtins.__import__")
    def test_config_set_complex_json_value(self, mock_import):
        """Test config set with complex JSON value"""
        # Mock the EphapticOS module
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.config.set = MagicMock()
        mock_import.return_value = mock_EphapticOS

        command = ConfigCommand()
        complex_json = '{"nested": {"key": "value"}, "array": [1, 2, 3]}'
        complex_json_expected_value = {"nested": {"key": "value"}, "array": [1, 2, 3]}
        args = argparse.Namespace(config_action="set", key="complex_config", value=complex_json)

        command.execute(args)
        mock_EphapticOS.config.set.assert_called_once_with(
            "complex_config", complex_json_expected_value, persist=True
        )

    @patch("builtins.__import__")
    def test_config_set_invalid_json_value(self, mock_import):
        """Test config set with invalid JSON value"""
        # Mock the EphapticOS module
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.config.set = MagicMock()
        mock_import.return_value = mock_EphapticOS

        command = ConfigCommand()
        invalid_json = '{"invalid": json}'
        args = argparse.Namespace(config_action="set", key="test_key", value=invalid_json)

        command.execute(args)
        mock_EphapticOS.config.set.assert_called_once_with("test_key", invalid_json, persist=True)

    @patch("EphapticOS.cli.commands.config_command.fmt.confirm")
    def test_config_unset_unknown_key(self, mock_confirm):
        """Test config unset with unknown key"""
        # Mock the EphapticOS module
        mock_EphapticOS = MagicMock()

        with patch.dict(sys.modules, {"EphapticOS": mock_EphapticOS}):
            command = ConfigCommand()
            args = argparse.Namespace(config_action="unset", key="unknown_key", force=False)

            mock_confirm.return_value = True

            # Should show error for unknown key
            command.execute(args)

        mock_confirm.assert_called_once()

    @patch("builtins.__import__")
    def test_config_unset_method_not_found(self, mock_import):
        """Test config unset when method doesn't exist on config object"""
        # Mock config object without the expected method
        mock_EphapticOS = MagicMock()
        mock_EphapticOS.config = MagicMock()
        # Don't set the set_llm_provider method
        mock_import.return_value = mock_EphapticOS

        command = ConfigCommand()
        args = argparse.Namespace(config_action="unset", key="llm_provider", force=True)

        # Should handle AttributeError gracefully
        command.execute(args)
        mock_EphapticOS.config.unset.assert_not_called()

    def test_config_invalid_subcommand(self):
        """Test config command with invalid subcommand"""
        command = ConfigCommand()
        args = argparse.Namespace(config_action="invalid_action")

        # Should handle unknown subcommand gracefully
        command.execute(args)


class TestGeneralEdgeCases:
    """Test general edge cases that apply to multiple commands"""

    def test_command_with_none_args(self):
        """Test command execution with None args"""
        commands = [
            AddCommand(),
            SearchCommand(),
            EphaptifyCommand(),
            DeleteCommand(),
            ConfigCommand(),
        ]

        for command in commands:
            # Should not crash with None args, though it might raise exceptions
            try:
                command.execute(None)
            except (AttributeError, CliCommandException):
                # Expected behavior for None args
                pass

    def test_parser_configuration_with_none_parser(self):
        """Test parser configuration with None parser"""
        commands = [
            AddCommand(),
            SearchCommand(),
            EphaptifyCommand(),
            DeleteCommand(),
            ConfigCommand(),
        ]

        for command in commands:
            # Should not crash, though it might raise AttributeError
            try:
                command.configure_parser(None)
            except AttributeError:
                # Expected behavior for None parser
                pass

    def test_command_properties_are_strings(self):
        """Test that all command properties are proper strings"""
        commands = [
            AddCommand(),
            SearchCommand(),
            EphaptifyCommand(),
            DeleteCommand(),
            ConfigCommand(),
        ]

        for command in commands:
            assert isinstance(command.command_string, str)
            assert len(command.command_string) > 0

            assert isinstance(command.help_string, str)
            assert len(command.help_string) > 0

            if hasattr(command, "description") and command.description:
                assert isinstance(command.description, str)

            if hasattr(command, "docs_url") and command.docs_url:
                assert isinstance(command.docs_url, str)

    @patch("tempfile.NamedTemporaryFile")
    def test_commands_with_temp_files(self, mock_temp_file):
        """Test commands that might work with temporary files"""
        # Mock a temporary file
        mock_file = MagicMock()
        mock_file.name = "/tmp/test_file.txt"
        mock_temp_file.return_value.__enter__.return_value = mock_file

        # Test AddCommand with temp file
        command = AddCommand()
        parser = argparse.ArgumentParser()
        command.configure_parser(parser)

        args = parser.parse_args([mock_file.name])
        assert args.data == [mock_file.name]
