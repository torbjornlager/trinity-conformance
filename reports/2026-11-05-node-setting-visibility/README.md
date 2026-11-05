# Native node-setting visibility and RELATION admission

All **47 final probes pass**: 32 in native SWI and 15 in native Trealla.
The [results](final/results.json) identify exact sources and the
[adapter](../../adapters/node_setting_visibility.py). These are disposable
development nodes, not a public deployment certificate.

Both runtimes now pass real RELATION HTTP enumeration, bound values, absent
family/private keys, invalid keys, mismatched values and repeatable reads in
blacklist, whitelist and off modes. Queries are plain `node_setting/2` calls;
the fixture does not advertise that predicate, load an application wrapper, or
use ISOBASE helpers such as `findall/3` to bypass the RELATION endpoint.
The adapter compares key sets externally, requires every configured value and
rejects duplicate answers or unfinished continuations.

SWI additionally passes changes through its actual owner admin API. Four
API families are disabled individually, restored, then disabled and restored
together: stateless, private database, session and actor APIs. Their keys
disappear and return with their original values. General settings remain.
The edits affect only the chosen node and profile: another ACTOR node in the
same process and the RELATION listener retain their own settings. Owner
configuration snapshots before and after public reads remain identical.
The local fixtures explicitly grant development admin capability; no live
node or real credential is used.

Trealla's family mapping is fixed by profile. Its RELATION checks complement
the prior [314-case settings matrix](../2026-11-05-whitelist-helper-admission/settings-final/results.json)
for ISOBASE, ISOTOPE and ACTOR. Unknown/unavailable settings fail; no fictional
policy-edit API or unavailable setting values were added. Its repeatability
checks compare the public relation; SWI also compares the owner configuration.

## Repair and regression checks

The [corrected pre-repair baseline](baseline/results.json) has 31 passes and
16 failures. Every failure is SWI rejecting `node_setting/2` at the separate
RELATION query-pattern filter, including the profile-isolation control that
queries a RELATION listener. Trealla already passes its endpoint checks and
SWI already passes the ACTOR family-policy probes. Baseline and final runs
use the same adapter hash.

The SWI repair adds only `node_setting/2` to RELATION admission. Existing family,
profile, source and sandbox checks continue afterward. Five maintained tests
check HTTP conjunctions in all sandbox modes, nonbinding admission, rejection
of wrappers/other arities, source-loading rejection, and disabling/re-enabling
the introspection family itself. Disabling that family still denies the call.
The tests do not admit arbitrary Prolog goals to RELATION.

The [focused selection](focused-final.txt) passes all five cases. The
[broader checks](regressions.txt) pass LINT, portable TEXT, all 1065 T4_NATIVE
tests, and HTTP visitor-ownership controls. The [conformance runner](runner-tests.txt)
passes all 104 tests; both ledger validators pass. Trealla runtime code is
unchanged in this batch. No manuscript or release/deployment pin changed.

## Fixture diagnostics

The [first run](first/results.json) had a fixture bug: `Counter(expected)`
treated dictionary values as expected multiplicities. The intended comparison
is `Counter(expected.keys())`. Its exact
[adapter snapshot](first-adapter.py.txt) and outcomes are retained separately.
The corrected baseline above isolates the actual runtime failures.

The [first focused unit run](focused-initial.txt) expected a profile-error
message when the owner disabled introspection. The implementation correctly
denied the call as an unavailable served relation. The assertion was corrected
to require denial naming `node_setting`, followed by successful restoration;
no runtime policy was relaxed.

## Ledger boundary and reproduction

B-346 now has scoped passing evidence for both native targets, joining their
existing B-339–B-345 evidence. Both native targets have 42 verified source
units in the 383-unit inventory. These counts are not percentages of language
conformance. GNU and both browser modes still lack `node_setting/2`; other
source/toplevel and lifetime obligations remain separately unverified.

[Verification metadata](verification.json) records source/adapter hashes,
commands, counts and committed revisions. From the conformance checkout, use
a fresh output directory:

```sh
python3 adapters/node_setting_visibility.py --swipl /usr/local/bin/swipl \
  --tpl /Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
  --swi-root /Users/lager/swi-prolog-node --trealla-root /Users/lager/trealla-port \
  --output /tmp/node-setting-visibility-new
```

From the SWI checkout:

```sh
SWIPL=/usr/local/bin/swipl tools/test.sh LINT TEXT T4_NATIVE
```
