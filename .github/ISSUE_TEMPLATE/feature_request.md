---
name: Feature Request
about: Suggest a new stress workload or a gap probe to add to the suite
title: ""
labels: enhancement
assignees: ""
---

**What would this stress?**
EigenGauntlet earns its keep by running small *real* workloads that surface
EigenScript language/runtime/stdlib/tooling gaps — not synthetic microbenchmarks.
Which part of the language or runtime would a new workload exercise (a builtin, a
concurrency path, an I/O primitive, an observer idiom, …)?

**Proposed workload / gap probe**
What real task it models, roughly how it'd run, and what gap you expect it to
surface. Keep it small enough to run quickly on constrained hardware (larger
modes must be opt-in and named, e.g. `--size 3`).

**Alternatives considered**
Any existing suite (tensor/dataflow/swarm/concurrent/parser/memory/observer/io/
realtime/module-scope) that already covers part of this.
