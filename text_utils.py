#Text processing utilities for cleaning and transforming Apache JIRA data

import re
from html import unescape
from typing import Dict, Any

def clean_text(text: str) -> str:
    #Clean and normalize text content
    if not text:
        return ""
    # Remove extra whitespace
    text = " ".join(text.split())
    return text.strip()

def remove_html_tags(html_text: str) -> str:
    #Remove HTML tags and decode HTML entities
    if not html_text:
        return ""
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', html_text)
    # Decode HTML entities
    text = unescape(text)
    return clean_text(text)

def transform_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    #Transform a raw issue into cleaned format
    fields = issue.get('fields', {})
    return {
        'key': issue['key'],
        'summary': clean_text(fields.get('summary', '')),
        'description': remove_html_tags(fields.get('description', '')),
        'status': fields.get('status', {}).get('name', ''),
        'created': fields.get('created', ''),
        'comments': [
            {
                'author': comment.get('author', {}).get('displayName', ''),
                'text': remove_html_tags(comment.get('body', '')),
                'created': comment.get('created', '')
            }
            for comment in fields.get('comment', {}).get('comments', [])
        ]

    }
