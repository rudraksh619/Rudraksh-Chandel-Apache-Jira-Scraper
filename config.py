
#Configuration and constants for Apache JIRA scraper

import os
import json
from typing import Dict, Any

# API endpoints
JIRA_BASE = "https://issues.apache.org/jira"
SEARCH_API = JIRA_BASE + "/rest/api/2/search"
ISSUE_API = JIRA_BASE + "/rest/api/2/issue/{issue_key}"
COMMENTS_API = JIRA_BASE + "/rest/api/2/issue/{issue_key}/comment"

# Scraping settings
PAGE_SIZE = 100  # maxResults per page
DEFAULT_PROJECTS = ["TIKA", "ZOOKEEPER", "OPENNLP"]

# Output directories and files
OUTDIR = "data"
RAW_DIR = os.path.join(OUTDIR, "raw")
STATE_FILE = os.path.join(OUTDIR, "state.json")
TRAIN_FILE = os.path.join(OUTDIR, "train.jsonl")

def ensure_dir(path: str):
    #Create directory if it doesn't exist
    os.makedirs(path, exist_ok=True)

def save_state(state: Dict[str, Any]):
    #Save scraping state to track progress
    ensure_dir(os.path.dirname(STATE_FILE))
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def load_state() -> Dict[str, Any]:
    #Load saved state if it exists
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)

    return {}
