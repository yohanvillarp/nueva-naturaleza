import os
import requests

body = os.getenv("ISSUE_BODY", "").lower()
issue_number = os.getenv("ISSUE_NUMBER")
repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Lógica de Validación (Ingeniería de Requisitos)
keywords = ["como", "quiero", "para"]
ambiguous_terms = ["rápido", "fácil", "bien", "mejor"]

has_structure = all(word in body for word in keywords)
is_ambiguous = any(term in body for term in ambiguous_terms)
is_valid = has_structure and not is_ambiguous

# URLs de la API de GitHub
label_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"

if not is_valid:
    # Si falla, añadimos las etiquetas de error
    requests.post(label_url, json={"labels": ["RQA-FAILED", "AMBIGUOUS"]}, headers=headers)
    print("Estado: Calidad Insuficiente. Etiquetas aplicadas.")
else:
    # SI ES VÁLIDO: Intentamos borrar la etiqueta RQA-FAILED si existe
    delete_url = f"{label_url}/RQA-FAILED"
    response = requests.delete(delete_url, headers=headers)
    
    if response.status_code == 204:
        print("Estado: Calidad Verificada. Etiqueta RQA-FAILED removida.")
    else:
        print("Estado: Calidad Verificada. No había etiquetas de error que remover.")