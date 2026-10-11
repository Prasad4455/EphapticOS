import warnings
import sys


def _load_server_main():
    """Import the heavy server module lazily.

    Importing server eagerly at package-import time pulls in the MCP SDK
    and uvicorn/starlette, which aren't available in environments that
    only depend on the core EphapticOS library (e.g. the unit-tests CI job).
    Deferring the import lets `import src.EphapticOS_client` succeed without
    those dependencies.
    """
    try:
        from .server import main as server_main
    except ImportError as relative_import_error:
        # The fallback exists for source checkouts where `src` isn't a package.
        # But it also used to swallow a missing third-party dependency: with
        # fastmcp absent, the real "No module named 'fastmcp'" was replaced by
        # a baffling "No module named 'server'". Re-raise the original when the
        # fallback fails too, so the actual cause is what the user sees.
        try:
            from server import main as server_main
        except ImportError:
            raise relative_import_error from None
    return server_main


def main():
    """Deprecated main entry point for the package."""
    import asyncio

    deprecation_notice = """
DEPRECATION NOTICE
The CLI entry-point used to start the EphapticOS MCP service has been renamed from
"EphapticOS" to "EphapticOS-mcp". Calling the old entry-point will stop working in a
future release.

WHAT YOU NEED TO DO:
Locate every place where you launch the MCP process and replace the final
argument EphapticOS → EphapticOS-mcp.

For the example mcpServers block from Cursor shown below the change is:
{
  "mcpServers": {
    "EphapticOS": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/EphapticOS-mcp",
        "run",
        "EphapticOS"              // <-- CHANGE THIS to "EphapticOS-mcp"
      ]
    }
  }
}

Continuing to use the old "EphapticOS" entry-point will result in failures once it
is removed, so please update your configuration and any shell scripts as soon
as possible.
"""

    warnings.warn(
        "The 'EphapticOS' command for EphapticOS-mcp is deprecated and will be removed in a future version. "
        "Please use 'EphapticOS-mcp' instead to avoid conflicts with the main EphapticOS library.",
        DeprecationWarning,
        stacklevel=2,
    )

    print("⚠️  DEPRECATION WARNING", file=sys.stderr)
    print(deprecation_notice, file=sys.stderr)

    asyncio.run(_load_server_main()())


def main_mcp():
    """Clean main entry point for EphapticOS-mcp command."""
    import asyncio

    asyncio.run(_load_server_main()())
