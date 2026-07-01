# Security Policy

`EigenGauntlet` is a suite of pure-EigenScript stress workloads. It opens no
network sockets by default and takes no untrusted input — it runs its own small
workloads on the EigenScript interpreter to surface language/runtime gaps. The
realistic attack surface is small, but reports are welcome.

## Reporting a vulnerability

Please report security issues privately rather than in a public issue — via
[GitHub private vulnerability reporting](https://github.com/InauguralSystems/EigenGauntlet/security/advisories/new)
or by contacting the maintainer at the address on the
[InauguralSystems](https://github.com/InauguralSystems) profile
(`contact@inauguralsystems.com`, subject prefix `[SECURITY]`). Include steps to
reproduce and the affected EigenScript version.

## Scope

- Issues in the EigenScript interpreter, runtime, or standard library belong in
  the [EigenScript](https://github.com/InauguralSystems/EigenScript) repository,
  which has its own security process.
- `EigenGauntlet`'s own scope is the `.eigs` workloads and the test runners.

## Supported versions

The latest tag on `main` is supported. `EigenGauntlet` tracks the pinned
EigenScript version it is tested against; run against that or newer.
