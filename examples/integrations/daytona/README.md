# EphapticOS memory handover on Daytona sandboxes

The [Daytona](https://www.daytona.io/) port of the
[Docker Sandboxes kit](../docker-sandbox-kit/): a supervisor agent and a worker
agent, each in its own cloud sandbox, handing persistent EphapticOS memory to each
other under EphapticOS's per-user ACLs. Everything runs embedded inside the
sandboxes; there is no EphapticOS server.

The payload is the **same** `supervisor_worker_handover.py` the Docker demo
uses (it is read from `../docker-sandbox-kit/demo/`, not copied). What this
directory adds is the Daytona orchestration, `handover.py`.

## How the handover works here

Docker Sandboxes move the EphapticOS state between two long-lived sandboxes with
`sbx cp`. Daytona can **fork** a running sandbox into a copy-on-write clone of
its filesystem, so the handover is the fork itself — no snapshot copying, no
shared mount:

```
snapshot "EphapticOS-memory"           debian-slim + EphapticOS, built once, reused
  └─ EphapticOS-supervisor  --phase brief    private note + briefing, grant worker read/write, emit token
       └─ fork: EphapticOS-worker  --phase work     recall by UUID, prove denials, write report
            └─ fork: EphapticOS-review  --phase review   supervisor recalls the worker's report
```

Each fork carries the whole EphapticOS state (SQLite users/ACLs, one `.lbug` graph
and one `.lance.db` vector store per dataset) on sandbox-local disk. The worker
receives everything on disk, exactly like the `sbx cp` snapshot in the Docker
demo — and exactly like there, what it can *read* is gated by EphapticOS's ACLs:
the private dataset raises `PermissionDeniedError`, the shared dataset is
reachable by UUID only (dataset names are namespaced per user), and the report
is written back with `dataset_id=`.

## Mapping the sbx kit onto Daytona

| Docker Sandboxes kit (`spec.yaml`) | Daytona (`handover.py`) |
|---|---|
| `credentials.proxyManaged` + `inject` on `api.openai.com` | organization **Secret** `EphapticOS-openai` with `hosts=["api.openai.com"]`, mounted via `secrets={"LLM_API_KEY": "EphapticOS-openai"}`. The sandbox sees an opaque placeholder; the proxy substitutes the key on requests to that host only. |
| `sbx policy init deny-all` + `permissions.network.allow` | `domain_allow_list="api.openai.com,extension.ladybugdb.com,raw.githubusercontent.com"`. PyPI is not on it: EphapticOS is installed at snapshot build time, not inside the sandbox. |
| `setup.install` (`uv tool install EphapticOS` on every sandbox creation) | a **Snapshot** built once with `Image.debian_slim("3.12").pip_install("EphapticOS")`; every sandbox in the chain starts from it warm. |
| `environment.variables` | passed per `exec` (`DATA_ROOT_DIRECTORY`, `SYSTEM_ROOT_DIRECTORY`, `LLM_MODEL`, `TELEMETRY_DISABLED`, `ENABLE_BACKEND_ACCESS_CONTROL=true`). |
| `agentInstructions` appended to the agent's memory file | no Daytona equivalent — Daytona has no agent-kit layer. Drop a `CLAUDE.md`/`AGENTS.md` into the work dir with `sandbox.fs.upload_file` when you run a real agent instead of the payload. |
| `sbx cp` state in and out of each sandbox | `sandbox.fork()` |
| `sbx policy log` | none locally; the script probes egress from inside the sandbox instead (`example.com` must be unreachable, `$LLM_API_KEY` must be the placeholder). |

Not used on purpose: Daytona **Volumes**. They are S3-backed FUSE mounts, the
same class of storage the Docker demo had to move away from (embedded LanceDB
would not run on the shared virtiofs workspace). Keep EphapticOS's embedded
databases on sandbox-local disk; a volume is fine for the handover token or
other plain files.

## Run it

```console
$ pip install daytona
$ export DAYTONA_API_KEY=...          # https://app.daytona.io
$ export LLM_API_KEY=sk-...           # first run only: creates the host-scoped Secret
$ python handover.py                  # ~1 min snapshot build the first time, then the 3 phases
$ python handover.py --keep           # leave the sandboxes up to inspect them
$ python handover.py --rebuild        # rebuild the snapshot after a EphapticOS release
```

Output ends with the dataset UUID that crossed the user boundary and the token
in `handover-out/handover_token.json`. Phase output is printed when each phase
finishes (`remember` builds a knowledge graph, so `brief` and `work` take a
few minutes each).

Inspecting a kept sandbox:

```python
from daytona import Daytona

sb = Daytona().get("EphapticOS-review")
print(sb.process.exec("printf '%s' \"$LLM_API_KEY\"").result)  # the placeholder, never a key
print(sb.process.exec("ls ~/EphapticOS-state/system/databases/").result)  # EphapticOS_db + per-owner dirs
```

Cleanup: the script deletes the three sandboxes unless `--keep` is passed. The
snapshot and the Secret are kept for the next run.

## Notes

- The Secret is scoped to `api.openai.com`. Using another provider means a
  different `hosts=` list, a different `LLM_MODEL`, and its API host on the
  domain allow list — see the [provider docs](https://docs.EphapticOS.ai/).
- `handover.py` re-applies `update_secrets` and `update_network_settings` on
  every fork instead of assuming the child inherits them; if Daytona changes
  that behaviour the demo keeps its guarantees.
- For concurrent agents that need live shared memory rather than a sequential
  handover, run a central EphapticOS API server (see
  `distributed/deploy/daytona_sandbox.py`) and put its host on each sandbox's
  domain allow list.

## Layout

```
daytona/
├── handover.py        # snapshot → supervisor → fork → worker → fork → review
├── handover-out/      # the JSON handover token (created at runtime)
└── README.md
```
