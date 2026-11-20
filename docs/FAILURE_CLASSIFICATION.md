# Failure classification

Every failing conformance result starts as `unclassified`. Investigation may
assign exactly one of these classifications:

| Identifier | Meaning |
|---|---|
| `protocol_implementation_defect` | The candidate's Web Prolog or ACTOR implementation violates an agreed observable contract. |
| `runtime_defect` | The underlying Prolog runtime prevents correct behaviour or crashes on a valid operation. |
| `deliberately_unsupported` | The candidate does not implement the behaviour and does not claim the profile that requires it. This normally produces runner status `unsupported`, not `fail`. |
| `specification_ambiguity` | The implementations disagree and the profile does not yet determine which result is required. |

A classification is a diagnostic conclusion, not a way to turn a failure
into a pass. Runtime workarounds may make a case pass, but the associated
upstream issue should remain linked from the report or implementation ledger.

The runner accepts a JSON object mapping case IDs to classification objects:

```json
{
  "AC-004": {
    "classification": "runtime_defect",
    "issue": "https://example.invalid/upstream/123",
    "note": "Guarded receive loses its arithmetic built-in"
  }
}
```

Only failing cases use this mapping. Passing results remain `pass`, and a
candidate that advertises less than the required profile is `unsupported`.

## Current issue triage

[CURRENT_ISSUES.md](../CURRENT_ISSUES.md) and its
[machine inventory](../backlog/current.json) preserve original result statuses
and group repeated evidence into work queues. A queue is not a demonstrated
single root cause. `open` means unresolved evidence, which may still need
fixture, protocol or contract diagnosis before runtime attribution.

The separate `production_disposition` records reviewed follow-up evidence:
`repaired_deployed`, `correct_preconditions_verified`, `superseded_assertion`,
`fixture_precondition`, `passing_replay_cause_open` and
`blocked_precondition`. None changes a raw result into `pass`. Candidate
repairs use `candidate_disposition: verified_not_deployed` and leave the
production finding open. Blocked live projections are separate from the
versioned input rows without execution anywhere.

Decisions in [backlog/decisions.json](../backlog/decisions.json) select exact
files/cases/candidates and require matching evidence. The generator rejects
missing, conflicting or hash-modified proof. It records source hashes and
JSON pointers, retains excluded profile/harness rows for audit, and never
writes historical report directories.

Current monitor selections use `monitor-contracts-0.2` and
`monitor-preflight-0.2`. Their predecessor files are preserved as historical
versions. The author-directed URI-text decision in the demonstrator's
`DEVIATIONS.md` (17 November 2026) supersedes the older atom-only proposal.
A historical failure against that proposal is a test contract mismatch,
not proof of an implementation violation of the newer rule.

For owned HTTP prompt verification, use `adapters/local_http_prompts.py`.
It explicitly enables standalone Trealla retained HTTP routes. The maintained
`runner/prompt_http.py` probes spawn/halt once before running assertions. A
failed preflight produces an error plus blocked cases and a nonzero exit;
it never certifies a missing endpoint or executes nineteen doomed assertions.
