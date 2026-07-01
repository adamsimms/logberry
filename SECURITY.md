# Security Policy

## Reporting a vulnerability

**Do not open a public GitHub issue for security problems.**

Report vulnerabilities privately through [GitHub private vulnerability reporting](https://github.com/adamsimms/driftwood/security/advisories/new). You can also use the repository **Security** tab and choose **Report a vulnerability**. Only maintainers can see submitted reports.

Include:

- A description of the issue
- Steps to reproduce
- Impact assessment (if known)

## What must never be committed

- Passwords, API keys, tokens, or private keys
- Wi-Fi credentials (`wpa_supplicant.conf`, NetworkManager connection files)
- Personal email addresses tied to machine config
- Gallery-specific install values that identify a private venue (if sensitive)
- Runtime data files: `data/tide_data.csv`, `data/wave_status.csv`
- Local notes (`scratchpad.md`, `.env`)

Use `config/data_input.py` and `config/gallery_hours.py` for install-specific values. Keep machine-local overrides out of git.

## Deployment guidance

- Do not expose the Pi's SSH port to the public internet without key-based auth and a firewall.
- Run motor and data services as the `pi` user, not as root (except for systemd install steps).
- Review `deploy/systemd/` unit files before enabling on your system.
- External data APIs (CHS IWLS, SmartAtlantic ERDDAP) are read-only public endpoints; no API keys are required.
