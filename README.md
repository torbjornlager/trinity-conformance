# Trinity conformance tests

This repository is the future implementation-neutral conformance suite for
Web Prolog nodes. Its purpose is to test observable behaviour, independently
of whether a candidate node is implemented in SWI-Prolog, Trealla Prolog, or
another runtime.

## Status

This is an initial holding repository. It records the test inventory and the
portable test cases identified during the Trealla port, but it does not yet
contain an executable conformance runner. No implementation should currently
claim conformance based on this repository.

The first executable tranche should extract black-box cases from Trinity's
wire-level interoperability tier. Portable actor and toplevel API cases can
then be added behind small runtime adapters.

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

## Provenance and license

The initial inventory was derived from `trinity-demonstrator` and
`trealla-port`. See [NOTICE.md](NOTICE.md). This repository is distributed
under the [MIT License](LICENSE).
