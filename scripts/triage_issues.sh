#!/usr/bin/env bash
# Close stale 2018 issues on adamsimms/driftwood with triage comments.
#
# Requires: gh CLI authenticated with issues write access
# Usage: ./scripts/triage_issues.sh

set -euo pipefail

REPO="adamsimms/driftwood"

close_issue() {
  local number="$1"
  local comment="$2"
  echo "Closing #$number..."
  gh issue close "$number" --repo "$REPO" --comment "$comment"
}

close_issue 10 "Resolved in the 2026 repository cleanup. The project now has README.md, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, install script, systemd setup docs, and API health checks."

close_issue 9 "Closing as out of scope for the software repository. Domain registration (driftwood.as) is a separate infrastructure decision and was not pursued in the codebase."

close_issue 11 "Closing as a future enhancement. For now:
- systemd captures service output via \`journalctl -u driftwood-data -u driftwood-motors\`
- \`scripts/check_apis.py\` verifies data sources
- Errors print to stdout in both scripts

Reopen if structured file logging is needed for a future exhibition."

close_issue 12 "Partially addressed. The repo now includes systemd units (\`deploy/systemd/\`) with \`Restart=on-failure\` for both data and motor services. Automatic Pi reboot on error is not implemented — use the optional cron reboot in the README if needed. Reopen if a dedicated watchdog/recovery sequence is required."

close_issue 14 "Closing as a future enhancement. Current options:
- Local: Ctrl+C in \`project_log_live.py\` prompts N (resume) or Q (runs \`closing_action()\`)
- systemd: \`sudo systemctl stop driftwood-motors\` (may not run the full closing sequence)

A dedicated remote graceful-shutdown signal (e.g. flag file or socket) could be added in a future PR. Reopen if needed."

close_issue 16 "The workaround described here (\`closing_action()\` + \`starting_act()\`) remains in \`scripts/motor_session.py\` when wave pacing fails. Motor code was refactored in 2026 and data APIs were migrated to CHS IWLS + SmartAtlantic ERDDAP. Reopen if position drift recurs during a live run."

echo "Adding resolution note to closed #1..."
gh issue comment 1 --repo "$REPO" --body "Done in the 2026 cleanup: install parameters moved to \`config/data_input.py\` and gallery hours to \`config/gallery_hours.py\`."

echo "Done. Open issues remaining:"
gh issue list --repo "$REPO" --state open
