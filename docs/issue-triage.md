# Issue triage (June 2026)

This documents the cleanup of stale 2018 issues after the repository rename to [adamsimms/driftwood](https://github.com/adamsimms/driftwood).

## Open issues reviewed

| # | Title | Action | Reason |
|---|-------|--------|--------|
| 10 | Documentation | **Close** | Addressed by README, CONTRIBUTING, SECURITY, CHANGELOG |
| 9 | Figure out domain | **Close** | Out of scope for the code repo |
| 11 | Logging | **Close** | Future enhancement; use `journalctl` for now |
| 12 | Reset log and restart Pi | **Close** | Partially addressed via systemd `Restart=on-failure` |
| 14 | Graceful remote stop | **Close** | Future enhancement; local Ctrl+C + Q works |
| 16 | Blank wave motor position | **Close** | Workaround remains in `motor_session.py`; reopen if bug recurs |

## Run the cleanup

The cloud agent token cannot close issues (403). Run locally with your GitHub credentials:

```bash
chmod +x scripts/triage_issues.sh
./scripts/triage_issues.sh
```

## Closed issues (2018)

Issues #1–#8 and #13, #15 were already closed. No changes needed.
