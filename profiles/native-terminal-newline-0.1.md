# Native newline regression selection

Run `runner/run.py --ws-url ws://HOST:PORT/ws --manifest
cases/native-terminal-newline-0.1.json --report /tmp/newline.json` on disposable
native ACTOR endpoints in blacklist and whitelist sandbox modes.

IO-001 checks direct and literal higher-order `nl/0`. IO-002 checks a child
using its inherited terminal. Opaque computed goals and private-helper admission
remain separate policy tests. Normal child monitor events may accompany output. Every case must emit a
terminal output event and complete deterministically. Output is acknowledged
through the public WebSocket protocol. Legacy native `data` may represent the
newline as empty text; when a peer supplies `stdout`, its exact content must
be one newline. These checks do not require a specific chunk count.

The six `cases/toplevel-waits-0.1.json` assertions use `runner/baseline.py`.
The two transferred edits make missing synchronous barrier/termination replies
throw explicitly instead of allowing later unification to hide the timeout.
