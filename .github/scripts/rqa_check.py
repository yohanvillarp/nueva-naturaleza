import os
import requests

body = os.getenv("ISSUE_BODY", "").lower()
issue_number = os.getenv("ISSUE_NUMBER")
repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

# Reglas básicas de RQA (Software Quality Requirements)
keywords = ["como", "quiero", "para"]
is_valid = all(word in body for word in keywords) and len(body) > 50

headers = {"Authorization": f"token {token}"}
url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"

if is_valid:
    requests.post(url, json={"labels": ["RQA-PASSED"]}, headers=headers)
else:
    # Si no cumple, ponemos etiqueta de error y comentamos el motivo
    requests.post(url, json={"labels": ["RQA-FAILED", "AMBIGUOUS"]}, headers=headers)
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    requests.post(comment_url, json={"body": "❌ Requisito rechazado por ambigüedad. Use el formato estándar."}, headers=headers)