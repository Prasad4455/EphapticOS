"""Guardrail: the DB worker subprocesses must NOT import EphapticOS.

This regressed silently in the past (old SubprocessGraphDBWrapper /
SubprocessVectorDBWrapper wrapped EphapticOS adapter classes in the child,
dragging the entire ~200 MB EphapticOS import graph into every child).

The new design puts worker code under the top-level ``EphapticOS_db_workers``
package, which by construction imports only the native DB library (kuzu or
lancedb) + pyarrow + stdlib. This test enforces that invariant by spawning a
clean Python child and verifying ``EphapticOS`` is absent from ``sys.modules``.
"""

from __future__ import annotations

import multiprocessing as mp
import sys

import pytest

# These tests construct subprocess workers explicitly, so the
# *_SUBPROCESS_ENABLED=false the Windows CI jobs set cannot keep them from
# spawning. On Windows the spawned child intermittently deadlocks at
# interpreter startup (a python.exe frozen at ~3.8 MB that never signals
# ready) and pytest hangs on it until the job timeout -- observed with the
# watchdog on runs 33643650, 33648260941 and 33729891452. Tracked as
# SDK-540; unskip these when its fix lands. Full coverage continues on the
# ubuntu and macOS legs.
pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="explicit worker spawn deadlocks intermittently on Windows (SDK-540)",
)


def _probe_kuzu_worker(result_q):
    # Import the worker; make sure ``EphapticOS`` isn't dragged in.
    import EphapticOS_db_workers.kuzu_worker

    EphapticOS_modules = sorted(m for m in sys.modules if m == "EphapticOS" or m.startswith("EphapticOS."))
    result_q.put(EphapticOS_modules)


def _probe_lancedb_worker(result_q):
    import EphapticOS_db_workers.lancedb_worker

    EphapticOS_modules = sorted(m for m in sys.modules if m == "EphapticOS" or m.startswith("EphapticOS."))
    result_q.put(EphapticOS_modules)


def _probe_harness(result_q):
    import EphapticOS_db_workers.harness

    EphapticOS_modules = sorted(m for m in sys.modules if m == "EphapticOS" or m.startswith("EphapticOS."))
    result_q.put(EphapticOS_modules)


def _run_probe(target) -> list:
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=target, args=(q,))
    p.start()
    try:
        return q.get(timeout=30)
    finally:
        p.join(timeout=10)
        if p.is_alive():
            p.terminate()
            p.join(timeout=5)


def test_kuzu_worker_does_not_import_EphapticOS():
    modules = _run_probe(_probe_kuzu_worker)
    assert modules == [], (
        f"Kuzu worker pulled EphapticOS into the child's sys.modules: {modules}. "
        "Keep the worker module (EphapticOS_db_workers.kuzu_worker) free of "
        "EphapticOS imports."
    )


def test_lancedb_worker_does_not_import_EphapticOS():
    # Skip gracefully if lancedb isn't installed in this environment.
    try:
        import lancedb
    except ImportError:
        pytest.skip("lancedb not installed")

    modules = _run_probe(_probe_lancedb_worker)
    assert modules == [], (
        f"LanceDB worker pulled EphapticOS into the child's sys.modules: {modules}. "
        "Keep the worker module (EphapticOS_db_workers.lancedb_worker) free of "
        "EphapticOS imports."
    )


def test_harness_does_not_import_EphapticOS():
    modules = _run_probe(_probe_harness)
    assert modules == [], (
        f"Harness pulled EphapticOS into the child's sys.modules: {modules}. "
        "Keep EphapticOS_db_workers.harness stdlib-only."
    )
