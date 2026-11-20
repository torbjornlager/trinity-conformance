# URI/source transfer — first repair and triage, 20 November 2026

**A Trealla reflection repair is committed and qualified locally; production is unchanged.** Trealla `d1ad920` restores source-level `write/1` and `writeln/1` through public `clause/2`, preserving variables shared with the clause head. The exact final regression fails against predecessor `e99126b` and passes against the candidate. N5 still runs `e99126b`; this report does not close its NU-011 finding.

## Evidence and scope

| Run | Result | Meaning |
|---|---|---|
| Original owned adapter, unchanged 13 assertions per runtime | 12 pass / 14 fail | Before this repair; original fixture configuration retained |
| Explicit alias-credential control, preliminary reflection candidate | 17 pass / 9 fail | Same assertion goals; both exact URL spellings explicitly authorized |
| Final maintained adapter and final source, macOS | 17 pass / 9 fail | No case/helper-program expectations changed |
| Final maintained adapter and final source, Linux | 17 pass / 9 fail | Same remaining nine observations |
| Complete final Trealla unit suite | 112/112 on macOS and 112/112 on Linux | Same 30-second watchdog per check; no watchdog relaxed |
| Conformance runner unit tests with Node 22.23.4 | 123/123 | Existing assertions unchanged |

NU-011 now passes in both native directions on both platforms. The dedicated regression checks blacklist, whitelist and off modes; original operation names; head/body and repeated-argument sharing; recopied private source; and preservation of variable terminal options. Blacklist/whitelist still deny runtime-clause inspection and stream output. Off mode deliberately has no query sandbox, so those denials are not asserted there. Runtime terminal output and transport authorization are unchanged.

## Separating the failures

**Missing fixture peer credentials.** Credentials are keyed by exact logical URL. The old adapter configured plain URLs but tested trailing-slash URLs as well. The corrected adapter explicitly authorizes both spellings on its disposable loopback peers and records the authorized URLs. It changes neither production settings nor credential matching rules. This clears the original owned SWI NU-009/012/013 and Trealla NU-008 observations. In particular, nested copied output round trips successfully when its return URL is authorized. This is not evidence that arbitrary unconfigured live aliases are authorized.

**Transport context versus local context.** Four explicit diagnostic controls confirm that an implicit local spawn is visible to its originating client, while a spawn through the same server's public URL uses a separate transport context and is not in the original `actors/1` namespace. The latter matches documented receiving-connection-plus-lineage ownership. NU-001/002/004 mix a local-visibility expectation with URI checks, so they need to be split/versioned before drawing a runtime conclusion. No runtime context or ordinary-name isolation was changed. An initial diagnostic used explicit `node(localhost)` and hit the fixture's remote-destination sandbox allowlist; the corrected control uses the implicit local spawn. Both are retained.

**Remaining address behavior.** Even with authorized aliases, NU-006 fails the canonical returned-address check on both engines. Trealla NU-003 also misses the monitor notification after a qualified local send with a trailing slash. These remain unresolved. They should be tested with one controlled actor and explicit node spellings before deciding how address normalization interacts with exact peer credentials and topology mappings. Live N7's fixture-creation rejections and GNU/N6 URI errors are separate pending investigations.

## Qualification history

The first reflection patch passed the complete 112-group suites, but review found that a structural pattern could bind an otherwise pending terminal-options argument. The final patch uses exact identity checks, adds a non-binding regression and repeats both complete suites. The published final logs and source manifest refer to this final version. An early new test incorrectly expected sandbox denial in off mode; that fixture error is retained separately and corrected according to the existing policy. The final regression itself is also run against the old runtime, where it fails on the missing source-level reflection.

The historical sweep and prior reports remain immutable. The current inventory may classify only the four explicitly reproduced owned credential-precondition observations; the Trealla repair is candidate evidence, not a deployed pass. This is not a fresh complete sweep or a deployment qualification. Next steps are to split the self-URL context cases, repair and qualify canonical address routing, then qualify a combined release against exact production images before updating live pins.

[Raw outcome summary](SUMMARY.json) · [artifact hashes](files-sha256.json).
