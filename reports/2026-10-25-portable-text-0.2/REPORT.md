# Portable-text specification and test expansion

25 October 2026. Scope: specification, test procedures and disposable-fixture
observations. Runtime code, installed runtimes, n3/n5 and book examples are
unchanged. The pending Boolean/URI runtime edits were excluded by archiving
committed source revisions for the test fixtures.

## Specification

[Experimental draft 0.2](../../profiles/portable-text-0.2.md) defines a character
as a Unicode scalar value, distinguishes graphemes from list elements and
forbids implicit normalization. `src_list/1` receives constructed clauses and
preserves numeric data and variable relationships. It does not recursively
convert code lists. Double quotes inside textual goals/options are handled by
the enclosing reader before the source loader receives the terms.

The [26-case manifest](../../cases/portable-text-0.2.json) retains the original
seven IDs/metadata and adds Unicode, option/input readers, constructed terms,
private/copied/DCG/URI source and peer/serialization coverage. Source policies
are explicitly configured only for the disposable loopback fixture. Neither
reader flags nor runtime sources are changed to make the experiment pass.

## Observations and limits

See the [matrix](COVERAGE.md) and raw reports. **SWI passes 4/26; Trealla passes
20/26** in the two tested configurations. These are draft failures, not newly
introduced failures of an ACTOR requirement.

- SWI's native-string convention conflicts with the proposed list semantics
  on most cases. It passes atom distinction, constructed `src_list` preservation,
  peer-source semantics against Trealla and remote term/sharing preservation.
- SWI TXT-015 is blocked by a sandbox rejection of a qualified internal DCG
  helper. That result does not isolate DCG source literal semantics. It remains
  a recorded failure, with no runtime repair attempted.
- Trealla TXT-008/020/025/026 return
  `representation_error(character)` from `read_term_from_atom/3`. This identifies
  rejection on the tested query-reading path, not the responsible engine or
  adapter component. TXT-020 cannot reach its answer round trip; TXT-026 cannot
  reach its input prompt because its query also contains a supplementary atom.
  Thus neither establishes whether the later boundary would independently
  accept or reject that scalar. TXT-019 does exercise ASCII input successfully.
- Trealla TXT-014 returns `instantiation_error` rather than completing the
  constructed-clause control. The test combines runtime source construction,
  admission, copying and sharing; it does not establish where that error arises.
  It must not be reported as proof that Trealla converts numeric lists.
- Trealla TXT-023 contacts the default SWI peer, where the assertion that the
  supplied literal is `[a,b]` fails. The reverse direction passes. The assertion
  runs **on the peer before serialization**, preventing quoted wire output from
  disguising different source-reader semantics. This is a configuration-pair
  difference, not evidence of a Trealla-local source-reader defect.
- Both URI source fetches returned HTTP 200; Trealla's URI assertion passes,
  while SWI's fails. There is no URI-policy waiver in either result.

No investigation or repair of those separate findings belongs to this batch.
The selected BMP combining/no-normalization cases pass on Trealla; that is not
proof of full Unicode support. Invalid UTF-8, surrogate rejection by nodes,
other term-input/option readers, direct remote ACTOR source transport, GNU,
browser runtimes, performance and migration of native-library calls remain
unmeasured. See the draft's migration gate before adopting any runtime change.

## Reproduction and preservation

The [fixture adapter](../../adapters/local_portable_text.py) archives committed
SWI source `786737f3352c9a3abc3f59c6e09a393008579b5a` and Trealla source
`7220bb562cf510d5cb12093fe84e7da73b5ecc86`. Pending source edits are recorded as
excluded inputs. [Provenance](provenance.json) includes archive hashes, commands,
binary hashes, fixture configuration and exact test-input hashes. The
[engine versions](engine-versions.json) record the separate SWI 10.1.18 candidate
and unmodified Trealla v3.14.10. SWI includes previously verified core and HTTP
shutdown changes; these are existing inputs, not changes made by this batch.

To rerun, select those revisions in disposable source checkouts and invoke:

```sh
python3 adapters/local_portable_text.py \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/selected/swi-prolog-node \
  --trealla-root /path/to/selected/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/portable-text-results
```

The adapter uses each checkout's HEAD and excludes its working-tree edits.
Temporary source archives are removed and both owned node processes are stopped.
[Preservation checks](preservation.json) pass for source files, separate engine
binaries/libraries, the dependency pin and live n3/n5 identities.
[Installed runtime targets/hashes](installed-preservation.json) still match the
preceding preservation record. No production source permissions are changed.

All 47 runner regression tests pass. New checks cover original manifest metadata,
fixture preflight, surrogate metadata, unchanged constructed clauses, input reply
ordering, round-trip spelling, rejection of executable reply suffixes, and peer
assertion placement. Report schema/accounting and whitespace checks also pass.
