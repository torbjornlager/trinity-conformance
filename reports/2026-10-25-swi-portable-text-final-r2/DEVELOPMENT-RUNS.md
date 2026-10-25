# Development records

Only the final-r2 configured/control reports feed this matrix. Earlier records
created during this batch are retained as development evidence:

- `...-candidate`: initial adapter mistakenly used the ACTOR runner for baseline
  manifests. Those KeyErrors are harness failures, not node failures.
- `...-configured` / `...-default-control`: peer trust was not configured for
  delegated remote actors; both readers show the same permission errors. The
  early default control also detects intentional overlapping source edits.
- `...-final` / `...-default-final`: explicit loopback trust; intermediate
  native-string writer rejection still present in the SWI source overlay.
- `...-unmodified-trealla`: separately reported Unicode limitation control.
- `...-final-r2` / `...-default-r2`: retained runtime implementation, proper
  runner dispatch, explicit loopback peer trust, stable source/engine snapshots.

The native test logs separately retain and explain the removed writer-rejection
experiment, full native-tier findings and focused follow-ups. Historical reports
from before this batch are unchanged.
