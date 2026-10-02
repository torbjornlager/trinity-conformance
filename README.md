# Trinity conformance tests

This repository is the future implementation-neutral conformance suite for
Web Prolog nodes. Its purpose is to test observable behaviour, independently
of whether a candidate node is implemented in SWI-Prolog, Trealla Prolog, or
another runtime.

## Status

The executable draft profiles are
[`actor-core-0.1`](profiles/actor-core-0.1.md) and
[`portable-text-0.1`](profiles/portable-text-0.1.md). The dependency-free
black-box runner contains cases exercised against both the SWI and Trealla
nodes. These remain drafts: passing one means only that a candidate passes its
explicitly listed cases.

## Profiles

The reference implementation currently recognizes these cumulative public
node profiles:

| Profile | Required public surface |
|---|---|
| `relation` | Restricted relational queries through `/call` |
| `isobase` | Stateless queries through `/call` |
| `isotope` | ISOBASE plus stateful `/toplevel_*` sessions |
| `actor` | ISOTOPE plus the Web Prolog WebSocket actor protocol |

`workbench` is also recognized by the reference implementation, but is an
unrestricted development mode rather than an initial portability target.

## Intended structure

- `cases/` — implementation-neutral case definitions and expected outcomes
- `adapters/` — thin process-launch and local-API adapters
- `docs/` — profile, provenance, and source-test inventories
- `reports/` — dated baseline and candidate-node reports
- `profiles/` — versioned observable contracts
- `runner/` — candidate-neutral external-node runner
- `schemas/` — machine-readable report formats

Implementation-specific unit tests remain in their implementation
repositories. In particular, SWI PlUnit internals and Trealla regression tests
do not belong here unless they are recast as an observable contract.

## Result vocabulary

An eventual runner should distinguish:

- `pass` — the advertised contract was observed
- `fail` — the candidate advertised the profile but violated the contract
- `unsupported` — the candidate does not advertise the required profile
- `not_applicable` — the case does not apply to this candidate configuration

Untested behaviour must never be counted as passing, and an unsupported
higher profile must not make a lower-profile implementation appear broken.

## Running ACTOR Core 0.1

The runner uses only the Python 3 standard library and connects to an already
running node. It never imports implementation code.

```sh
python3 runner/run.py \
  --ws-url ws://127.0.0.1:3060/ws \
  --advertised-profile actor \
  --candidate trealla-local \
  --report reports/trealla-local.json
```

For a private node, keep the secret out of the command line:

```sh
export TRINITY_TEST_TOKEN='...'
python3 runner/run.py \
  --ws-url wss://node.example/ws \
  --token-env TRINITY_TEST_TOKEN \
  --candidate node-name
```

Use `--case AC-004` to select one case. Failure classifications can be added
with `--classifications path/to/classifications.json`; see
[`docs/FAILURE_CLASSIFICATION.md`](docs/FAILURE_CLASSIFICATION.md).

To test the opt-in portable-text draft without changing the node:

```sh
python3 runner/run.py \
  --manifest cases/portable-text-0.1.json \
  --ws-url ws://127.0.0.1:3060/ws \
  --advertised-profile actor \
  --candidate candidate-name
```

The `actor` argument in this invocation describes the transport surface used
by the current runner. It does not claim that portable-text semantics are part
of the deployed ACTOR profile.

The cross-runtime implications for SICStus, Ciao, XSB, and the systems already
considered are recorded in
[`docs/PORTABLE_TEXT_PORTABILITY.md`](docs/PORTABLE_TEXT_PORTABILITY.md).

## Provenance and license

The initial inventory was derived from `trinity-demonstrator` and
`trealla-port`. See [NOTICE.md](NOTICE.md). This repository is distributed
under the [MIT License](LICENSE).
