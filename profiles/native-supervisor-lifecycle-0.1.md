# Native supervisor lifecycle

Run `cases/native-supervisor-lifecycle-0.1.json` with
`adapters/local_runtime_contracts.py` on native SWI and Trealla in blacklist,
whitelist and owner-off. The paired runtime lifecycle changes are prerequisites.

The cases cover source-free and private-source startup/inspection, respawn
ordering, idle application goals, busy child shutdown, copied private helper
context, owned monitor preservation and failed source preparation without name
publication. Native barrier tests gate child preparation and prove creation
and name publication wait for it; native halt tests inject queued normal and
abnormal notifications alongside acknowledgements. The busy server wire test
first waits for the callback's entry message before testing halt completion.

Private framework entry probes run only under sandbox policies. Computed
entries are probed in blacklist; whitelist may reject opaque goals before
execution. Every rejection also requires same-session recovery. No private
guard or trusted framework entry is supplied as user source. This selection
contains no child-ID or stopped-child count assertions; those have a separate
selection and depend on these lifecycle fixes. No deployed-node or WASM
qualification is claimed.
