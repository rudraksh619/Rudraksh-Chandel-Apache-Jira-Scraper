import argparse
import json
import os
from typing import List

from jira_scraper import ApacheJiraFetcher
from text_utils import transform_issue
from config import (
    DEFAULT_PROJECTS, RAW_DIR, TRAIN_FILE, 
    ensure_dir, save_state, load_state
)

def scrape_projects(projects: List[str], transform_only: bool = False):
    #Scraping and processing
    state = load_state()
    processed_issues = state.get('processed_issues', set())

    if not transform_only:
        jira = ApacheJiraFetcher()
        for project in projects:
            print(f"Processing project: {project}")
            project_dir = os.path.join(RAW_DIR, project)
            ensure_dir(project_dir)
            
            for issue in jira.process_project(project):
                issue_key = issue['key']
                if issue_key in processed_issues:
                    continue
                
                # Save raw issue data
                issue_file = os.path.join(project_dir, f"{issue_key}.json")
                with open(issue_file, 'w', encoding='utf-8') as f:
                    json.dump(issue, f, indent=2)
                
                processed_issues.add(issue_key)
                save_state({'processed_issues': list(processed_issues)})

    # Transform and combine all issues
    ensure_dir(os.path.dirname(TRAIN_FILE))
    with open(TRAIN_FILE, 'w', encoding='utf-8') as out:
        for project in projects:
            project_dir = os.path.join(RAW_DIR, project)
            if not os.path.exists(project_dir):
                continue
            
            for filename in os.listdir(project_dir):
                if not filename.endswith('.json'):
                    continue
                    
                with open(os.path.join(project_dir, filename), encoding='utf-8') as f:
                    issue = json.load(f)
                    transformed = transform_issue(issue)
                    out.write(json.dumps(transformed) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Apache JIRA Scraper')
    parser.add_argument('--projects', nargs='+', default=DEFAULT_PROJECTS,
                      help='JIRA project keys to scrape')
    parser.add_argument('--transform-only', action='store_true',
                      help='Skip scraping, only transform existing data')
    args = parser.parse_args()
    
    scrape_projects(args.projects, args.transform_only)

if __name__ == '__main__':

    main()
