# Rudraksh Singh Chandel - E22CSEU0668 - Bennett University
# Apache JIRA Scraper

A simple tool to scrape and process issues from Apache's public JIRA instance.

## Features

 Handles pagination automatically
 Built-in rate limiting to avoid server overload
 Saves raw JSON for every issue (for reproducibility)
 Cleans and transforms text (removes HTML & normalizes content)
 Resumable scraping — remembers processed issues
 Fault-tolerant with retry logic
 Outputs clean JSONL dataset ready for LLMs

## Setup

1. Make sure you have Python installed

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run with default projects (TIKA, ZOOKEEPER, OPENNLP):

```bash
python main.py
```

Run with specific projects:

```bash
python main.py --projects HADOOP SPARK KAFKA
```

Transform existing data without scraping:

```bash
python main.py --transform-only
```

## Output

The script creates two types of output:

1. Raw data: `data/raw/<PROJECT>/<ISSUE>.json`
   - Contains complete JSON data for each issue
   - Organized by project folders

2. Processed data: `data/train.jsonl`
   - One JSON object per line
   - Contains cleaned and transformed issue data
   - Includes: key, summary, description, status, comments
   - Example of a cleaned JSON line (one per line in `data/train.jsonl`)

```json
{
"key": "TIKA-123",
"summary": "Example summary",
"description": "Cleaned description text.",
"status": "Resolved",
"created": "2020-01-01T00:00:00.000+0000",
"comments":
[
{"author": "User Name",
"text": "Helpful comment.",
"created": "2020-01-02T00:00:00.000+0000"}
]
}
```

## Project Structure

- `main.py` - Main script to run
- `jira_scraper.py` - Handles JIRA API interaction
- `text_utils.py` - Text cleaning and transformation

- `config.py` - Configuration and constants

## Design and reasoning

I kept the code simple and readable. Each file has one job.

- Single-threaded scraping keeps behavior predictable and avoids aggressive load on the public API.
- Retry + small sleeps make the scraper more polite and reduce failures.
- Saving raw JSON helps debugging and lets you re-run transformations without re-downloading.

## Edge cases handled

- Paging: fetches pages until no more issues are left.
- 429/Rate-limit safety: retries and pauses between pages reduce chance of being throttled.
- Network errors: transient failures are retried by the HTTP session configuration.
- Missing data: transformer uses defaults so missing fields won't crash the run.
- Clean text output: HTML tags stripped and HTML entities decoded for readable text.
- Partial runs: processed issue keys are saved so a stopped run can resume.
