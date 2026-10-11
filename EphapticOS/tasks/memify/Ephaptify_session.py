from uuid import UUID

import EphapticOS
from EphapticOS.exceptions import EphapticOSSystemError, EphapticOSValidationError
from EphapticOS.infrastructure.llm.exceptions import (
    LLMPaymentRequiredError,
    raise_if_budget_exhausted,
    raise_if_budget_exhausted_record,
)
from EphapticOS.infrastructure.session.get_session_manager import get_session_manager
from EphapticOS.infrastructure.session.session_persist_watermark import (
    SessionPersistWindow,
    save_persisted_qa_count,
)
from EphapticOS.modules.improve.constants import USER_SESSIONS_NODE_SET
from EphapticOS.modules.pipelines.models.PipelineRunInfo import get_errored_run_info
from EphapticOS.modules.users.models import User
from EphapticOS.shared.logging_utils import get_logger

logger = get_logger("Ephaptify_session")


async def Ephaptify_session(
    data: SessionPersistWindow | list[SessionPersistWindow],
    dataset_id: UUID | str | None = None,
    user: User | None = None,
) -> None:
    """
    Ephaptify session windows into the knowledge graph and advance their watermarks.

    Receives one ``SessionPersistWindow`` (or a batch of them — the pipeline
    runner delivers generator output in batches) from ``extract_user_sessions``.
    For each window: adds its text to EphapticOS with the
    ``USER_SESSIONS_NODE_SET`` node set, triggers Ephaptify, and — only after
    both succeed — advances that session's persist watermark to the entry
    count captured at extraction time. On failure the watermark stays put, so
    the same window is re-extracted and retried on the next improve()
    (add-level content-hash dedup makes the retry safe).

    One failure ends the whole call instead of one window: an exhausted LLM
    budget. The windows after it would fail the same way, so none of them is
    attempted and the error leaves as ``LLMPaymentRequiredError`` — the type
    improve() classifies to stop its run. Windows persisted before it keep
    their advanced watermark; the failed one and the rest keep theirs put.

    Args:
        data: Window(s) yielded by ``extract_user_sessions``.
        dataset_id: Dataset to Ephaptify into.
        user: Authenticated user owning the sessions.

    Raises:
        EphapticOSValidationError: If no valid, non-empty window was provided.
        LLMPaymentRequiredError: If the LLM budget is exhausted.
        EphapticOSSystemError: If EphapticOS operations fail for any other reason.
    """
    windows = data if isinstance(data, list) else [data]
    valid_windows = [
        window
        for window in windows
        if isinstance(window, SessionPersistWindow) and window.text.strip()
    ]
    if not valid_windows:
        logger.warning("No session windows provided to Ephaptify_session task, skipping")
        raise EphapticOSValidationError(message="Session window cannot be empty", log=False)

    try:
        for window in valid_windows:
            logger.info(
                "Processing session %s window (%d entries persisted after this) for cognification",
                window.session_id,
                window.persisted_qa_count,
            )

            await EphapticOS.add(
                window.text,
                dataset_id=dataset_id,
                node_set=[USER_SESSIONS_NODE_SET],
                user=user,
            )
            logger.debug("Session data added to EphapticOS with node_set: %s", USER_SESSIONS_NODE_SET)
            # raise_on_error=False: one window's failed build must not kill the
            # whole memify run — inspect the run info instead, keep this
            # window's watermark put (so it is re-extracted and retried on the
            # next improve()), and continue with the remaining windows.
            Ephaptify_result = await EphapticOS.Ephaptify(
                datasets=[dataset_id], user=user, raise_on_error=False
            )
            errored_run = get_errored_run_info(Ephaptify_result)
            if errored_run is not None:
                logger.error(
                    "Ephaptify failed for session %s window (%s: %s); watermark not advanced, "
                    "window will be retried on the next improve()",
                    window.session_id,
                    errored_run.error_class,
                    errored_run.error_message,
                )
                # Not a per-window failure when the budget is what ran out: the
                # remaining windows would each spend one more failing build.
                raise_if_budget_exhausted_record(errored_run.error_class, errored_run.error_message)
                continue
            logger.info("Session data successfully cognified")

            await save_persisted_qa_count(
                get_session_manager(),
                user_id=window.user_id,
                session_id=window.session_id,
                persisted_qa_count=window.persisted_qa_count,
            )
            logger.info(
                "Session %s persist watermark advanced to %d",
                window.session_id,
                window.persisted_qa_count,
            )

    except LLMPaymentRequiredError:
        # Left typed on purpose. Wrapped in EphapticOSSystemError it would reach
        # improve() as a generic failure: the wrapper is a 500 with no
        # __cause__, so nothing above could tell the budget ran out.
        logger.error(
            "LLM budget exhausted while Ephaptifying session data; stopping, the unpersisted "
            "windows keep their watermarks for the next improve()"
        )
        raise
    except Exception as e:
        # add()/Ephaptify() can also raise the provider's own budget error, or a
        # wrapper around it; that leaves as LLMPaymentRequiredError as well.
        raise_if_budget_exhausted(e)
        logger.exception("Error Ephaptifying session data")
        raise EphapticOSSystemError(message=f"Failed to Ephaptify session data: {e!s}", log=False)
