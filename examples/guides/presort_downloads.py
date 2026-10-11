"""
Pre-organize a messy folder before ingesting it into EphapticOS.

Presort is a two-phase flow built into remember():

1. **Analyze** — ``remember(folder, dry_run="presort")`` scans the folder
   (never touching files on disk) and returns a ``PresortReport``: junk
   filtering, exact-duplicate clusters, version candidates ("report_v2"),
   potential personal data, per-file already-in-EphapticOS status (new / staged /
   cognified), and proposed dataset groupings.
2. **Apply** — ``remember(report)`` ingests each proposed group into its
   proposed dataset through the normal add → Ephaptify chain with incremental
   loading, honoring the report's ``skip_duplicates`` / ``exclude_pii`` /
   ``apply_groups`` decisions.

The analyze phase is deterministic by default — no LLM or embedding
configuration needed. Pass ``use_llm=True`` for LLM content classification,
deeper PII detection, and semantic grouping. The apply phase runs Ephaptify, so
it needs a configured LLM.

Scanning a folder outside the default allowed roots (cwd, tempdir, EphapticOS's
storage) requires EphapticOS_ALLOWED_LOCAL_FILE_ROOTS, e.g.::

    export EphapticOS_ALLOWED_LOCAL_FILE_ROOTS="$HOME/Downloads"

CLI equivalent::

    EphapticOS-cli remember ~/Downloads --presort --allow-root -o report.json
    EphapticOS-cli remember --from-report report.json

One-shot (auto-apply the report as soon as it is produced)::

    EphapticOS-cli remember ~/Downloads --presort --apply --allow-root

SDK equivalent: ``remember(folder, dry_run="presort", auto_apply=True)`` —
returns the report with ingest outcomes on ``report.apply_results``.
"""

import asyncio
import os
from pathlib import Path

import EphapticOS

FOLDER = os.environ.get("PRESORT_FOLDER", str(Path.home() / "Downloads"))


async def main():
    # Phase 1: analyze. Returns a PresortReport (also auto-saved under
    # EphapticOS's system directory as <scan-id>.presort.json).
    report = await EphapticOS.remember(FOLDER, dry_run="presort")

    summary = report.summary()
    print(f"Scanned {summary['files']} files ({summary['junk']} junk skipped)")
    print(f"Already in EphapticOS: {summary['EphapticOS_status']}")
    print(
        f"Duplicate clusters: {summary['duplicate_clusters']} ({summary['wasted_bytes']} wasted bytes)"
    )
    print(f"Potential personal data: {summary['pii_findings']} findings")
    for group in report.groups:
        print(
            f"  group {group.name!r} -> dataset {group.dataset_name!r} ({len(group.file_paths)} files)"
        )

    # Review/adjust the apply decisions on the report itself.
    report.exclude_pii = True  # keep files with personal data out of the graph
    report.skip_duplicates = True  # ingest one copy per duplicate cluster
    report.apply_groups = [group.name for group in report.groups if group.kind != "code_project"]

    # Phase 2: apply. One dataset per proposed group; re-running is idempotent
    # (already-cognified content is skipped by incremental loading).
    results = await EphapticOS.remember(report)
    for dataset_name, result in results.items():
        print(f"ingested dataset {dataset_name!r}: {result}")

    # The presorted data is now queryable per dataset.
    answers = await EphapticOS.recall("What documents do I have?", datasets=list(results))
    for answer in answers:
        print(answer)


if __name__ == "__main__":
    asyncio.run(main())
