import os
import requests
from typing import Dict, Any
from cururo.util.publisher import Publisher
from github import Github, Auth

class GitIssuePublisher(Publisher):

    def __init__(self, repo:str, _api_key:str, sha:str, user:str = None):
        super().__init__()
        _auth = Auth.Token(_api_key)
        self.github = Github(auth=_auth)
        self.repo = repo
        self.sha = sha
        self.user = user

    def __get_repo(self):
        return self.github.get_repo(self.repo)
    
    def publish(self, body: str):
        title = f"Automated Issue for {self.user};\n [commit {self.sha}]"
        return self.__get_repo().create_issue(title, body=body, assignee=self.user)
    
    def generate_report(self, data):
        report = [
            f"### Commit Review Summary\n",
            f"**Commit SHA:** {self.sha}\n",
            f"**Message:**\n- **Written:** {data['message']['message']}"
        ]

        # Add additional message details
        report.extend(
            f"- **{key.capitalize()}:** {value}" 
            for key, value in data['message'].items() if key != 'message'
        )

        # Code analysis section
        report.append("\n**Code Analysis:**\n")
        if 'complexity_comment' in data['code']:
            report.append(f"- **Complexity Comment:**\n  {data['code']['complexity_comment']}")


        # ACID sections
        if 'acid_score' in data['code'] and 'acid_comment' in data['code']:
            report.append("\n- **ACID Analysis:**")
            for acid_key, acid_score in data['code']['acid_score'].items():
                acid_comment = data['code']['acid_comment'].get(acid_key, "")
                report.append(f"  - **{acid_key.capitalize()}:** {acid_score}\n    *{acid_comment}*")

        # Vulnerable code section
        if 'vulnerable_code' in data['code']:
            report.append("\n**Vulnerable Code:**")
            report.append(f"- **Section:** \n  ```python\n  {data['code']['vulnerable_code']['section']}\n  ```")
            report.append(f"- **Comment:**\n  {data['code']['vulnerable_code']['comment']}")
            report.append(f"- **Score:** {data['code']['vulnerable_code']['score']}")

        return '\n'.join(report)
    

class WebPublisher(Publisher):

    def __init__(self, url:str, secret:str):
        super().__init__()
        self.url = url
        self.secret = secret

    def publish(self, data):
        return self.__send_request(data)

    def __send_request(self, data):
        headers = { 'Content-Type': 'application/json' }
        data['secret'] = self.secret
        res = requests.post(self.url, headers=headers, json=data)
        res.raise_for_status()
        return res

    def sort_data(self, data: Dict[str, Any], others: Dict[str, Any] = None) -> Dict[str, Any]:
        if others is None:
            others = {}
        sorted_data = {
            'message': data['message'].get('message', ''),
            'suggested': data['message'].get('suggested', ''),
            'adherence': data['message'].get('adherence', ''),
            'completeness': data['message'].get('completeness', ''),
            'atomicity': data['code']['acid_score'].get('a', ''),
            'consistency': data['code']['acid_score'].get('c', ''),
            'isolation': data['code']['acid_score'].get('i', ''),
            'durability': data['code']['acid_score'].get('d', ''),
            'vulnerability': data['code']['vulnerable_code'].get('score', ''),
        }
        sorted_data.update(others)
        return sorted_data
    