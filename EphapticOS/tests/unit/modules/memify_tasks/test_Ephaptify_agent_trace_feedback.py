import sys
from unittest.mock import AsyncMock, patch

import pytest

from EphapticOS.exceptions import EphapticOSSystemError, EphapticOSValidationError
from EphapticOS.infrastructure.session.session_persist_watermark import (
    TRACE_PERSIST_WATERMARK,
    TracePersistWindow,
)
from EphapticOS.tasks.memify.Ephaptify_agent_trace_feedback import Ephaptify_agent_trace_feedback

# The module object (not the re-exported function), for patching get_session_manager.
Ephaptify_agent_trace_feedback_module = sys.modules[
    "EphapticOS.tasks.memify.Ephaptify_agent_trace_feedback"
]


@pytest.mark.asyncio
async def test_Ephaptify_agent_trace_feedback_success():
    trace_content = "Session ID: trace_session\n\ndraft plan succeeded.\nwrite_summary failed."

    with (
        patch("EphapticOS.add", new_callable=AsyncMock) as mock_add,
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock) as mock_Ephaptify,
    ):
        await Ephaptify_agent_trace_feedback(trace_content, dataset_id="123")

    mock_add.assert_called_once_with(
        trace_content,
        dataset_id="123",
        node_set=["agent_trace_feedbacks"],
        user=None,
    )
    mock_Ephaptify.assert_called_once_with(datasets=["123"], user=None, raise_on_error=False)


@pytest.mark.asyncio
async def test_Ephaptify_agent_trace_feedback_forwards_user():
    """Test user is forwarded to EphapticOS.add/EphapticOS.Ephaptify."""
    trace_content = "Session ID: trace_session\n\ndraft plan succeeded."
    user = object()

    with (
        patch("EphapticOS.add", new_callable=AsyncMock) as mock_add,
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock) as mock_Ephaptify,
    ):
        await Ephaptify_agent_trace_feedback(trace_content, dataset_id="123", user=user)

    mock_add.assert_called_once_with(
        trace_content,
        dataset_id="123",
        node_set=["agent_trace_feedbacks"],
        user=user,
    )
    mock_Ephaptify.assert_called_once_with(datasets=["123"], user=user, raise_on_error=False)


@pytest.mark.asyncio
async def test_Ephaptify_agent_trace_feedback_custom_node_set_name():
    trace_content = "Session ID: trace_session\n\ndraft plan succeeded."

    with (
        patch("EphapticOS.add", new_callable=AsyncMock) as mock_add,
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock),
    ):
        await Ephaptify_agent_trace_feedback(
            trace_content,
            dataset_id="123",
            node_set_name="custom_trace_feedbacks",
        )

    mock_add.assert_called_once_with(
        trace_content,
        dataset_id="123",
        node_set=["custom_trace_feedbacks"],
        user=None,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("value", ["", "   \n\t  ", None])
async def test_Ephaptify_agent_trace_feedback_rejects_empty_input(value):
    with pytest.raises(EphapticOSValidationError, match="Agent trace content cannot be empty"):
        await Ephaptify_agent_trace_feedback(value)


@pytest.mark.asyncio
async def test_Ephaptify_agent_trace_feedback_add_failure():
    trace_content = "Session ID: trace_session\n\nfeedback"

    with (
        patch("EphapticOS.add", new_callable=AsyncMock) as mock_add,
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock),
    ):
        mock_add.side_effect = Exception("Add operation failed")

        with pytest.raises(EphapticOSSystemError, match="Failed to Ephaptify agent trace content"):
            await Ephaptify_agent_trace_feedback(trace_content)


@pytest.mark.asyncio
async def test_Ephaptify_agent_trace_feedback_Ephaptify_failure():
    trace_content = "Session ID: trace_session\n\nfeedback"

    with (
        patch("EphapticOS.add", new_callable=AsyncMock),
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock) as mock_Ephaptify,
    ):
        mock_Ephaptify.side_effect = Exception("Ephaptify operation failed")

        with pytest.raises(EphapticOSSystemError, match="Failed to Ephaptify agent trace content"):
            await Ephaptify_agent_trace_feedback(trace_content)


@pytest.mark.asyncio
async def test_Ephaptify_agent_trace_feedback_errored_run_info_does_not_raise():
    """An errored build (raise_on_error=False path) is logged, not raised,
    so one bad trace session can't kill the whole memify run."""
    from uuid import uuid4

    from EphapticOS.modules.pipelines.models.PipelineRunInfo import PipelineRunErrored

    errored = PipelineRunErrored(
        pipeline_run_id=uuid4(),
        dataset_id=uuid4(),
        dataset_name="ds",
        error_class="AuthenticationError",
        error_message="invalid api key",
    )

    with (
        patch("EphapticOS.add", new_callable=AsyncMock),
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock) as mock_Ephaptify,
    ):
        mock_Ephaptify.return_value = {"ds": errored}

        await Ephaptify_agent_trace_feedback("Session ID: trace_session\n\nfeedback")


# ----------------------------------------------------------------- watermark windows


class _FakeSessionManager:
    def __init__(self):
        self.rows: dict[str, list[dict]] = {}

    @property
    def store(self) -> list[dict]:
        return [row for rows in self.rows.values() for row in rows]

    async def get_session_context_entries(self, *, user_id, session_id=None):
        return list(self.rows.get(session_id, []))

    async def update_session_context_entry(self, *, user_id, entry_id, merge, session_id=None):
        for row in self.rows.get(session_id, []):
            if row.get("id") == entry_id:
                row.update(merge)
                return True
        return False

    async def create_session_context_entry(self, *, user_id, entry_dump, session_id=None):
        self.rows.setdefault(session_id, []).append(dict(entry_dump))
        return True


def _window(text="Session ID: s\n\nstep", persisted_trace_count=3, session_id="s"):
    return TracePersistWindow(
        user_id="u", session_id=session_id, text=text, persisted_trace_count=persisted_trace_count
    )


@pytest.mark.asyncio
async def test_window_advances_watermark_after_successful_Ephaptify():
    manager = _FakeSessionManager()
    window = _window(persisted_trace_count=5)

    with (
        patch("EphapticOS.add", new_callable=AsyncMock) as mock_add,
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock),
        patch.object(
            Ephaptify_agent_trace_feedback_module, "get_session_manager", return_value=manager
        ),
    ):
        await Ephaptify_agent_trace_feedback(window, dataset_id="123", user="user")

    mock_add.assert_called_once_with(
        window.text, dataset_id="123", node_set=["agent_trace_feedbacks"], user="user"
    )
    assert await TRACE_PERSIST_WATERMARK.read_count(manager, "u", "s") == 5


@pytest.mark.asyncio
async def test_batched_windows_each_advance_their_own_session():
    manager = _FakeSessionManager()
    windows = [
        _window(session_id="s1", persisted_trace_count=2),
        _window(session_id="s2", persisted_trace_count=7),
    ]

    with (
        patch("EphapticOS.add", new_callable=AsyncMock) as mock_add,
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock) as mock_Ephaptify,
        patch.object(
            Ephaptify_agent_trace_feedback_module, "get_session_manager", return_value=manager
        ),
    ):
        await Ephaptify_agent_trace_feedback(windows, dataset_id="123")

    assert mock_add.await_count == 2
    assert mock_Ephaptify.await_count == 2
    assert await TRACE_PERSIST_WATERMARK.read_count(manager, "u", "s1") == 2
    assert await TRACE_PERSIST_WATERMARK.read_count(manager, "u", "s2") == 7


@pytest.mark.asyncio
async def test_errored_run_info_keeps_watermark_put():
    from uuid import uuid4

    from EphapticOS.modules.pipelines.models.PipelineRunInfo import PipelineRunErrored

    manager = _FakeSessionManager()
    errored = PipelineRunErrored(
        pipeline_run_id=uuid4(),
        dataset_id=uuid4(),
        dataset_name="ds",
        error_class="AuthenticationError",
        error_message="invalid api key",
    )

    with (
        patch("EphapticOS.add", new_callable=AsyncMock),
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock) as mock_Ephaptify,
        patch.object(
            Ephaptify_agent_trace_feedback_module, "get_session_manager", return_value=manager
        ),
    ):
        mock_Ephaptify.return_value = {"ds": errored}
        await Ephaptify_agent_trace_feedback(_window(persisted_trace_count=5), dataset_id="123")

    assert await TRACE_PERSIST_WATERMARK.read_count(manager, "u", "s") == 0
    assert manager.store == []


@pytest.mark.asyncio
async def test_Ephaptify_exception_keeps_watermark_put():
    manager = _FakeSessionManager()

    with (
        patch("EphapticOS.add", new_callable=AsyncMock),
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock) as mock_Ephaptify,
        patch.object(
            Ephaptify_agent_trace_feedback_module, "get_session_manager", return_value=manager
        ),
    ):
        mock_Ephaptify.side_effect = Exception("Ephaptify operation failed")
        with pytest.raises(EphapticOSSystemError, match="Failed to Ephaptify agent trace content"):
            await Ephaptify_agent_trace_feedback(_window(persisted_trace_count=5), dataset_id="123")

    assert await TRACE_PERSIST_WATERMARK.read_count(manager, "u", "s") == 0


@pytest.mark.asyncio
async def test_blank_window_is_rejected_like_empty_text():
    with pytest.raises(EphapticOSValidationError, match="Agent trace content cannot be empty"):
        await Ephaptify_agent_trace_feedback([_window(text="   \n")])


@pytest.mark.asyncio
async def test_plain_text_never_touches_the_session_manager():
    def boom():
        raise AssertionError("plain text carries no watermark")

    with (
        patch("EphapticOS.add", new_callable=AsyncMock),
        patch("EphapticOS.Ephaptify", new_callable=AsyncMock),
        patch.object(Ephaptify_agent_trace_feedback_module, "get_session_manager", boom),
    ):
        await Ephaptify_agent_trace_feedback("Session ID: s\n\nfeedback", dataset_id="123")
