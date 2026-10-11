from unittest.mock import patch

import pytest

from EphapticOS.modules.observability.exceptions import UnsupportedObserverError
from EphapticOS.modules.observability.get_observe import get_observe
from EphapticOS.modules.observability.observers import Observer


def test_get_observe_raises_for_unsupported_observer():
    """Unsupported observer (e.g. LLMLITE, LANGSMITH) raises UnsupportedObserverError."""
    with patch("EphapticOS.modules.observability.get_observe.get_base_config") as get_config:
        get_config.return_value = type("Config", (), {"monitoring_tool": Observer.LLMLITE})()

        with pytest.raises(UnsupportedObserverError, match="Unsupported observer"):
            get_observe()
