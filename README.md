# Automated CPA Manager

A Selenium-based automation suite for managing CPA (Cost Per Action) marketing campaigns. It automates repetitive SiteGround hosting tasks — adding domains, uploading landing pages, enforcing HTTPS, and flushing cache — all driven by a Google Sheets tracker.

## Overview

Managing many CPA landing pages manually is tedious. This tool reads a Google Sheet that tracks domain status and automates the hosting workflow end-to-end using browser automation.

**Three standalone scripts, each handling a phase of the workflow:**

| Script | What it does |
|---|---|
| `DomainMaestro.py` | Registers unhosted domains on SiteGround, then uploads the correct landing page folder |
| `ContentUpdater.py` | Replaces content on already-hosted domains (deletes old files, uploads new ones) |
| `HTTPS_CacheCleaner.py` | Enforces HTTPS and flushes the dynamic cache for each domain |

The Google Sheet acts as the source of truth — each script reads domains filtered by a status column (e.g. `"Domain Added on Hosting" = FALSE`) and writes back `TRUE` after each successful operation.

## Architecture

```
automated-cpa-manager/
├── classes/
│   ├── SeleniumManager.py      # Chrome WebDriver wrapper (click, fill, wait, cookies)
│   ├── WebHostingManager.py    # SiteGround-specific automation (login, add domain, file manager)
│   ├── GoogleSheetsManager.py  # Read/write domain data from Google Sheets
│   └── DiskFileManager.py      # HTML content injection + zip packaging
├── functions/
│   ├── read_json_file.py       # JSON config loader
│   └── setup_logger.py         # Dual-handler logger (info.log + error.log)
├── data/                       # Gitignored — credentials and runtime data go here
├── DomainMaestro.py
├── ContentUpdater.py
├── HTTPS_CacheCleaner.py
├── config-example.json         # Template for config.json
└── requirements.txt
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Requires Python 3.8+ and [ChromeDriver](https://chromedriver.chromium.org/) matching your installed Chrome version.

### 2. Configure

Copy `config-example.json` to `config.json` and fill in your values:

```bash
cp config-example.json config.json
```

```json
{
    "sheet_credentials":   "data/your-service-account.json",
    "cookies":             "data/your-site-cookies.json",
    "local_storage":       "data/local_storage.json",
    "website_credentials": "data/website_credentials.json",
    "sheet_name":          "Your Sheet Name",
    "worksheet_index":     "0 1",
    "url":                 "https://eu.siteground.com/"
}
```

### 3. Credentials

Place the following files inside the `data/` directory (gitignored):

- **Google service account JSON** — from [Google Cloud Console](https://console.cloud.google.com/). The service account needs Editor access to your Google Sheet.
- **`website_credentials.json`** — SiteGround login:
  ```json
  { "email": "you@example.com", "password": "your-password" }
  ```
- **`cookies.json`** / **`local_storage.json`** — optional session data to skip the login flow (export from your browser's DevTools).

### 4. Google Sheet structure

Each worksheet needs at minimum a `Domain` column. The scripts look for these status columns and update them after each action:

| Column | Used by |
|---|---|
| `Domain Added on Hosting` | DomainMaestro |
| `Upload Folder` | DomainMaestro, ContentUpdater |
| `Name Changed` | DomainMaestro, ContentUpdater |
| `Enforce HTTPS` | HTTPS_CacheCleaner |
| `Flush Cache` | HTTPS_CacheCleaner |

### 5. Landing pages

Place landing page template folders under `data/landing_pages/<Type>/` where `Type` matches the value in your sheet's `Type` column. Each folder should contain an `index.html`. The tool injects the domain's `Full Name` into the `<title>` and `<h1 class="heading">` before uploading.

## Usage

Run whichever script matches your current workflow phase:

```bash
python DomainMaestro.py       # Add new domains + upload landing pages
python ContentUpdater.py      # Replace content on existing domains
python HTTPS_CacheCleaner.py  # Enforce HTTPS + flush cache
```

Logs are written to `info.log` and `error.log` in the project root.

## Tech Stack

- **Selenium 4** — browser automation
- **gspread** — Google Sheets API
- **BeautifulSoup4** — HTML content injection
- **Google Auth** — service account authentication
