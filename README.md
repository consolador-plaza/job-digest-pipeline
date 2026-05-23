# Job Digest Pipeline

Automated Gmail-to-Google-Sheets job aggregation pipeline.

Parses job alert emails from LinkedIn, Indeed, Glassdoor, and JobStreet, extracts structured job data, deduplicates results, stores them in Google Sheets, and tracks parser health metrics.

## Features

- Gmail API ingestion
- Multi-parser architecture
- LinkedIn parser
- Indeed parser
- Glassdoor parser
- JobStreet parser
- Google Sheets export
- Duplicate detection
- Gmail label workflow
- Parser health monitoring
- Run history logging
- Failure notifications
- ISO-8601 timestamps
- Gmail message traceability

## Pipeline Architecture

Gmail
  ↓
Loader
  ↓
Parser Detector
  ↓
Specific Parser
  ↓
Validation
  ↓
Deduplication
  ↓
Google Sheets Export
  ↓
Metrics + Notifications

## Project Structure

job_digest/

├── config/
├── dedup/
├── diagnostics/
├── export/
├── ingest/
├── logging_utils/
├── models/
├── notifications/
├── parsers/
├── reporting/
├── storage/
├── tests/
├── validation/
└── main.py

## Example Output

| Timestamp | Role | Company | Source | Gmail_ID |
|---|---|---|---|---|
| 2026-05-23T11:22:00 | Data Analyst | Accenture | LinkedIn | 19e4... |


## Setup

### Install

pip install -r requirements.txt

### Configure

Create `.env`

NOTIFY_EMAIL=your_email
NOTIFY_PASSWORD=app_password
NOTIFY_TO=your_email

### Run

python main.py

## Gmail Workflow

Incoming emails use label:

Jobs

Successful processing moves emails to:

Jobs Processed

Failures move emails to:

Jobs Failed

## Roadmap

### Completed

- Gmail ingestion
- Multi-parser routing
- Google Sheets export
- Deduplication
- Gmail_ID tracking
- ISO timestamps
- Parser metrics
- Notifications
- Secrets externalization

### Planned

- Dashboard
- Packaging
- CI/CD
- Docker support
- Historical analytics
