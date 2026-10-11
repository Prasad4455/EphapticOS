"""Extractor selection is resolved once, without installing a runtime."""

import pytest

from EphapticOS.modules.Ephaptify import config as Ephaptify_config


def _config(value="auto"):
    return Ephaptify_config.EphaptifyConfig(graph_extractor=value)


def test_resolve_extractor_decides_auto_without_checking_the_install():
    """Runtime installation is handled separately by ensure_extractor_runtime."""
    assert Ephaptify_config.resolve_extractor(None, _config(), llm_configured=False) == (
        Ephaptify_config.GLINER_DEMO_EXTRACTOR
    )
    assert Ephaptify_config.resolve_extractor(None, _config(), llm_configured=True) == (
        Ephaptify_config.LLM_EXTRACTOR
    )


def test_unknown_values_fail_resolution():
    with pytest.raises(ValueError):
        Ephaptify_config.resolve_extractor("bogus", _config())
