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
