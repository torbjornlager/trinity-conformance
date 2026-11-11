# Receive callback source context

The eleven cases in `receive-callback-context-0.1.json` run unchanged on native
SWI and Trealla in blacklist, whitelist and owner-off modes through
`adapters/local_runtime_contracts.py`. The existing source-copy selection adds
SCOPY-006: a copied controller creates a second-generation child whose guard
must infer the private relation and retain fallback behavior. All expected
receives have throwing deadlines; empty mailbox assertions deliberately use a
successful timeout and throw if an unexpected message appears.

Trealla's receive callback API dispatcher and copied-source restoration must
land alongside validated private-helper admission before requiring these cases.
Patterns remain ordinary data, bindings from unsuccessful guards roll back,
ordinary exceptions do not consume unmatched messages, and body alternatives
belong to a single consumed message. The port-specific native unit group also
rejects forbidden copied guards and access to private implementation bridges.

This selection checks ordinary guard exceptions. It does not replace the separate
held-RPC control-exception release fixture or claim browser/GNU qualification.
The runtime's source restoration keeps implementation bridges out of copied
application source. Retain the existing successor relation and source-boundary
regressions when combining these changes.
