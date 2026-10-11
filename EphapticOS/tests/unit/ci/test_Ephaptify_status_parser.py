"""Pin how the cloud benchmark reads one dataset's entry from ``datasets/status``.

The Ephaptify wait loop raises "Ephaptify errored on the tenant" from whatever the
tenant put in that entry, and three shapes reach it: a bare status string, the
nested ``{pipeline_name: status}`` map, and — with ``include_error_detail`` —
a Cloud tenant's ``{status, reason, error}`` object. The nightly was red for a
week with no cause in any log because the third shape was never requested; the
parser is what turns it into a readable failure, so each shape is covered here.
"""

import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
BENCH = ROOT / "EphapticOS/tests/performance/statistics_percentile/bench_EphapticOS.py"


@pytest.fixture(scope="module")
def Ephaptify_status():
    os.environ.setdefault("EphapticOS_LOG_FILE", "false")
    os.environ.setdefault("TELEMETRY_DISABLED", "1")
    spec = importlib.util.spec_from_file_location("bench_EphapticOS", BENCH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module._Ephaptify_status


def test_bare_status_string_passes_through(Ephaptify_status):
    assert Ephaptify_status("DATASET_PROCESSING_COMPLETED") == ("DATASET_PROCESSING_COMPLETED", "")


def test_missing_entry_is_no_status(Ephaptify_status):
    assert Ephaptify_status(None) == (None, "")


def test_nested_pipeline_map_reads_the_Ephaptify_pipeline(Ephaptify_status):
    assert Ephaptify_status({"Ephaptify_pipeline": "DATASET_PROCESSING_ERRORED"}) == (
        "DATASET_PROCESSING_ERRORED",
        "",
    )
    assert Ephaptify_status({"other_pipeline": "DATASET_PROCESSING_COMPLETED"}) == (None, "")


def test_detail_object_renders_reason_then_error(Ephaptify_status):
    status, detail = Ephaptify_status(
        {
            "status": "DATASET_PROCESSING_ERRORED",
            "reason": "insufficient_credits",
            "error": "LLMPaymentRequiredError: Budget has been exceeded! Current cost: 10.0, Max budget: 10.0",
        }
    )
    assert status == "DATASET_PROCESSING_ERRORED"
    assert detail == (
        " (insufficient_credits; LLMPaymentRequiredError: Budget has been exceeded!"
        " Current cost: 10.0, Max budget: 10.0)"
    )


@pytest.mark.parametrize(
    ("entry", "expected"),
    [
        ({"status": "DATASET_PROCESSING_ERRORED", "error": "boom"}, " (boom)"),
        (
            {"status": "DATASET_PROCESSING_ERRORED", "reason": "insufficient_credits"},
            " (insufficient_credits)",
        ),
        ({"status": "DATASET_PROCESSING_ERRORED", "reason": None, "error": None}, ""),
        ({"status": "DATASET_PROCESSING_ERRORED", "reason": "", "error": ""}, ""),
        ({"status": "DATASET_PROCESSING_COMPLETED"}, ""),
    ],
    ids=["error-only", "reason-only", "nulls", "empty-strings", "no-detail"],
)
def test_detail_object_skips_absent_and_empty_fields(Ephaptify_status, entry, expected):
    # The pod sends None for a field it has nothing for and the stored pipeline
    # error can be an empty string; neither may show up as "(; )" in the message.
    assert Ephaptify_status(entry) == (entry["status"], expected)


def test_non_string_detail_values_are_rendered(Ephaptify_status):
    assert Ephaptify_status({"status": "DATASET_PROCESSING_ERRORED", "error": {"code": 402}}) == (
        "DATASET_PROCESSING_ERRORED",
        " ({'code': 402})",
    )


class _FakeResponse:
    def __init__(self, payload):
        self.status = 200
        self._payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def json(self):
        return self._payload


class _FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get(self, url, params=None):
        self.calls.append((url, params))
        return _FakeResponse(self.payload)


class _FakeClient:
    service_url = "https://tenant.example"

    def __init__(self, payload):
        self.session = _FakeSession(payload)

    async def _get_session(self):
        return self.session


@pytest.fixture(scope="module")
def wait_for_cloud_Ephaptify(Ephaptify_status):
    # Same module object as the parser fixture; reach the loop through it.
    return Ephaptify_status.__globals__["_wait_for_cloud_Ephaptify"]


@pytest.mark.asyncio
async def test_wait_loop_asks_for_the_error_detail_and_reports_it(wait_for_cloud_Ephaptify):
    dataset_id = "f4dc8025-1a62-51eb-a874-6e885713dcb6"
    client = _FakeClient(
        {
            dataset_id: {
                "status": "DATASET_PROCESSING_ERRORED",
                "reason": "insufficient_credits",
                "error": "Budget has been exceeded! Current cost: 10.0, Max budget: 10.0",
            }
        }
    )
    started = {dataset_id: {"status": "PipelineRunStarted"}}

    with pytest.raises(RuntimeError) as raised:
        await wait_for_cloud_Ephaptify(client, started, poll_interval_s=0)

    assert str(raised.value) == (
        f"Ephaptify errored on the tenant for dataset {dataset_id}"
        " (insufficient_credits; Budget has been exceeded! Current cost: 10.0, Max budget: 10.0)"
    )
    (url, params) = client.session.calls[0]
    assert url == "https://tenant.example/api/v1/datasets/status"
    assert ("include_error_detail", "true") in params
    assert ("dataset", dataset_id) in params


@pytest.mark.asyncio
async def test_wait_loop_returns_once_every_dataset_completed(wait_for_cloud_Ephaptify):
    client = _FakeClient({"ds-1": "DATASET_PROCESSING_COMPLETED"})
    await wait_for_cloud_Ephaptify(
        client, {"ds-1": {"status": "PipelineRunStarted"}}, poll_interval_s=0
    )
    assert len(client.session.calls) == 1
