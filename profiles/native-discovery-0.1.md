# Shared discovery metadata

`adapters/native_discovery.py` runs the same eight assertions on actual native
SWI and Trealla /node_info endpoints in blacklist, whitelist and owner-off.
Owner source includes an import, an empty dynamic predicate, facts, rules,
a DCG and private/control exclusions. Live published services are distinguished
from ordinary private aliases. The fixture checks unregister, republish,
monitored termination, shared-source replacement and clear, plus private
session shadows and repeated metadata reads without re-running initialization.

The control actor is trusted fixture setup driven only through the subprocess
stdin pipe, with numbered file acknowledgements and bounded deadlines. It
adds no HTTP control route. SWI controller actors start only after listener
identity is established. The Trealla trusted compiled control entries use its
internal caller-context option; that option is never application source.
SWI reload retains imports and empty dynamic declarations, so owner setup
explicitly retires this fixture's two declarations on replacement. Both hosts
then have the same database state for the metadata assertions. This fixture
does not claim identical source-reload APIs across hosts. Before the private-shadow stage, Trealla uses the same declarations without
an initializer: shared source is replayed into each actor on that host. The
metadata-read stage and the native parser fixture cover initialization; this
selection does not qualify per-actor initializer replay. Different
initialization counts at initial host
setup are permitted; metadata reads themselves must not change the count.
The focused native Trealla unit fixture separately rejects executing owner
initialization merely to scan metadata at configuration time.

Use the two native root arguments, `--tpl` for the released Trealla engine,
and a fresh `--output` directory. All fixture listeners and credentials stay
local. The Trealla discovery runtime change must land before requiring this
selection. This is native qualification, with no browser or GNU coverage claim.
