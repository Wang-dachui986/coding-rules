# Security policy

`coding-rules` is an instruction and template skill for Codex. It does not run
a service, store user accounts, or ship application credentials. The sensitive
surface is whatever a project writes down while using the skill.

## Reporting a vulnerability

Please report vulnerabilities privately.

1. Open [a GitHub security advisory](https://github.com/Wang-dachui986/coding-rules/security/advisories/new) if private vulnerability reporting is enabled for this repository.
2. If that page says reporting is disabled, contact the maintainer [Wang-dachui986](https://github.com/Wang-dachui986) and ask for a private channel. Enabling private vulnerability reporting is a repository setting the maintainer controls.

Do not open a public issue, pull request, or discussion for a vulnerability.
Do not include live secrets, access logs, or a proof of concept that would
expose someone else's project.

## What to report

- A way the skill instructions cause secrets to be written into governance files, task cards, handoffs, or evidence
- A validator bypass that accepts secret-shaped content, a broken required file, or an R1–R3 handoff that takes over R0-only progress reporting
- A release or CI workflow that publishes more than the skill directory and `LICENSE`, or that leaks credentials from the build

Out of scope: a project's own product vulnerabilities, and Codex or GitHub
product defects. Report those to the product that owns them.

## Supported versions

No GitHub Release has been published yet. Until `v0.1.0` is tagged, the
maintained line is the `main` branch. After a release is published, only the
latest `v*` release and `main` are maintained.

## Secrets in governance files

The skill forbids passwords, tokens, private keys, cookies, full server
addresses, private URLs, user data, and raw access logs in rules, task cards,
evidence, and handoffs. If one of those lands in a file, remove it from the
current files and from git history before you open a public change. The
validator looks for a few secret-shaped patterns. It is not a secret scanner
for a whole product repository.
