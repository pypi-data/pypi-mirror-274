import os
import re
import json
import subprocess
import argparse
from .publishers import GitIssuePublisher, WebPublisher

def extract_message(text):
    pattern = r'\[C:START\](.*?)\[C:END\]'
    matcher = re.search(pattern, text, re.DOTALL)
    if matcher:
        return matcher.group(1)
    return None

def main(openai_key, assistant_id, token, repo, message, gh_before, sha, author, webhook, websecret):
    git_publisher = GitIssuePublisher(repo, token, sha, author)
    web_publisher = WebPublisher(webhook, websecret)

    try:
        diff = subprocess.check_output(['git', 'diff', gh_before, sha, "--word-diff"]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error generating git diff: {e}")
        return

    item = f'Commit Message: {message}\n\nCommit Diff: {diff}'

    try:
        note = subprocess.check_output([
            'cururo', 
            '--item', item, 
            '--openai-key', openai_key, 
            '--assistant-id', assistant_id,
            # '--mode', 'testing',
        ]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running cururo: {e}")
        return
    
    response = extract_message(note)
    if not response:
        print("No response extracted from the note.")
        return

    try:
        response = json.loads(response)
        response['message']['suggested'] = response['message']['message']
        response['message']['message'] = message
        git_publisher.publish(git_publisher.generate_report(response))
        web_publisher.publish(web_publisher.sort_data(response, {"user": author, "sha": sha, "repo": repo}))
    except json.JSONDecodeError:
        print(f"Error decoding JSON response: {response}")
        print(response)
    except Exception as e:
        print(f"Unexpected error: {e}")


        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Commit message and diff handler with OpenAI assistance.")

    #### Need tokens
    parser.add_argument('--openai-key', default=os.getenv('OPENAI_API_KEY'), help='OpenAI API key')
    parser.add_argument('--assistant-id', default=os.getenv('OPENAI_ASSISTANT_ID'), help='OpenAI assistant ID')
    parser.add_argument('--token', default=os.getenv('GH_TOKEN'), help='GitHub token')

    #### Commit id versions
    parser.add_argument('--gh-before', default=os.getenv('GH_BEFORE'), help='GitHub before SHA')
    parser.add_argument('--sha', default=os.getenv('SHA'), help='Commit SHA')

    #### Data of commit
    parser.add_argument('--repo', default=os.getenv('REPO'), help='Repository name')
    parser.add_argument('--message', default=os.getenv('MESSAGE'), help='Commit message')
    parser.add_argument('--author', default=os.getenv('AUTHOR'), help='Commit author')

    #### External Api to post
    parser.add_argument('--webhook', default=os.getenv('WEBHOOK'), help='Webhook URL')
    parser.add_argument('--websecret', default=os.getenv('WEBSECRET'), help='Webhook secret')

    args = parser.parse_args()

    main(args.openai_key, args.assistant_id, args.token, args.repo, args.message, args.gh_before, args.sha, args.author, args.webhook, args.websecret)
