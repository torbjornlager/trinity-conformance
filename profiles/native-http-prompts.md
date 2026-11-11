Native HTTP prompt regressions
==============================

Run runner/prompt_http.py with --swi and --trealla pointing to disposable local ACTOR endpoints. The suite exercises correlated replies, one-use references, malformed-input recovery, Abort/Halt races, competing replies, and visitor ownership. The endpoint fixtures must enable anonymous visitor identity and semi-stateful HTTP sessions. Keep saturation and racing probes off live nodes.

The cases are recorded in cases/prompt-http-0.1.json. WebSocket reply and profile-boundary checks are described in prompt-reply-regressions.md.
