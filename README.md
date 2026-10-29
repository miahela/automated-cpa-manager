# Automated CPA Manager

Python browser automation for managing landing pages on SiteGround from a Google Sheets tracker. It reduces repeated hosting setup and content updates, then records completed actions in the sheet.

| Script | Purpose |
|---|---|
| `DomainMaestro.py` | Add existing domains to hosting and upload landing pages. It does not purchase or register domains. |
| `ContentUpdater.py` | Delete existing website content and upload its replacement. |
| `HTTPS_CacheCleaner.py` | Enforce HTTPS and retry pending cache flushes independently. |

![Screenshot placeholder, replace with a redacted demo](docs/screenshot.png)

## Setup and run

Use Python 3.10+ and Chrome. Dependencies retain the original version pins; compatibility with newer Python and Chrome versions needs a live check. ChromeDriver must match Chrome and be available locally, or Selenium Manager needs network access to obtain it.

```powershell
cd C:\Users\miahlea\Desktop\Projects\automated-cpa-manager
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item config-example.json config.json
New-Item -ItemType Directory -Force data | Out-Null
Copy-Item samples\landing_pages data\landing_pages -Recurse
Copy-Item samples\website_credentials.example.json data\website_credentials.json
Copy-Item config\xpaths.example.json config\xpaths.json
```

Edit `config.json` with your sheet name, worksheet indexes (space-separated, starting at 0), URLs, and local file paths. Paths resolve relative to that config file. `.env.example` documents the optional `CPA_CONFIG` process environment variable; `.env` files are not loaded automatically.

Put a Google service account key at `data/service-account.json`, enable the Sheets and Drive APIs, and share your test spreadsheet with that account as Editor. Edit the local website credential file. Cookies and local storage are optional: leave their config values null or provide paths to exported JSON (a cookie list and a key/value object respectively).

The original `data/xpaths.json` was not included. `config/xpaths.example.json` lists every required selector key, with explicit placeholders. Copy it and replace every placeholder with a selector verified against your dashboard before running any workflow. No live selectors have been verified in this cleanup.

Import `samples/domains.csv` into a test sheet. All sample names and domains are fictional. Replace `landing.example` with a domain you control for a workflow test. Preserve all CSV headers and use literal TRUE/FALSE status cells. Each domain must appear once across configured worksheets, with no blank rows. `Type` selects `data/landing_pages/<Type>/index.html`; `Full Name` replaces the title and main heading. Use simple HTML templates with existing head, body, title and `h1.heading` tags.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe smoke_test.py
# After verifying selectors, credentials, and a disposable test domain:
.\.venv\Scripts\python.exe DomainMaestro.py
.\.venv\Scripts\python.exe ContentUpdater.py
.\.venv\Scripts\python.exe HTTPS_CacheCleaner.py
```

The three workflows make live changes. Both upload workflows delete existing hosting files. Back up the test site first. Run one script at a time. `smoke_test.py` only reads sheet statuses and opens the dashboard, without logging in or changing hosting content. Logs go to `info.log` and `error.log` in the working directory.

## Stack

Python, Selenium/Chrome, gspread, Google service account authentication, BeautifulSoup, and ZIP packaging. Dependencies are listed in `requirements.txt`.

## Known limits

- SiteGround selectors need re-verifying against the current UI before live use, including selectors embedded in the Python scripts. The original selector config is missing and must be supplied locally. MFA, CAPTCHA, and session expiry may interrupt runs.
- Offline regressions use mocked browser and API objects. They check local behavior, not live authentication, selectors, or upload completion. No network test was run during cleanup.
- Some hosting actions use fixed waits and report success when the browser sequence completes, without verifying the final remote state. Check the test site and sheet after a workflow run.
- Templates are edited in place, and uploads share one ZIP path. Keep a clean template backup and avoid concurrent runs.
- This is SiteGround-specific automation, not a general hosting client. No retry scheduler or rollback is included.
- Credentials, session exports, landing pages, local selector config, and generated archives are ignored by Git. Keep real client data out of tracked samples.
