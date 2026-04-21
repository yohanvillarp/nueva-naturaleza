import os
import requests

body = os.getenv("ISSUE_BODY", "").lower()
issue_number = os.getenv("ISSUE_NUMBER")
repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

<<<<<<< feat/rqa-bot-dashboard
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
=======
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
comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"

if not is_valid:
    # 1. Si falló, intentamos borrar RQA-PASSED (por si el usuario editó un issue bueno y lo arruinó)
    requests.delete(f"{label_url}/RQA-PASSED", headers=headers)
    
    # 2. Añadimos las etiquetas de error
    requests.post(label_url, json={"labels": ["RQA-FAILED", "AMBIGUOUS"]}, headers=headers)
    
    # 3. Dejamos un comentario de retroalimentación (Feedback SQA)
    error_msg = "❌ **Pipeline Bloqueado: Requisito ambiguo o sin estructura.**\nPor favor, usa el formato: *Como [rol], quiero [acción], para [beneficio]* y reemplaza adjetivos subjetivos por métricas exactas."
    requests.post(comment_url, json={"body": error_msg}, headers=headers)
    
    print("Estado: Calidad Insuficiente. Etiquetas y comentario aplicados.")

else:
    # 1. SI ES VÁLIDO: Borramos todas las etiquetas de error posibles
    requests.delete(f"{label_url}/RQA-FAILED", headers=headers)
    requests.delete(f"{label_url}/AMBIGUOUS", headers=headers)
    
    # 2. Añadimos la etiqueta de éxito
    requests.post(label_url, json={"labels": ["RQA-PASSED"]}, headers=headers)
    
    # 3. Dejamos un comentario de validación exitosa
    success_msg = "✅ **Calidad Verificada.**\nEste requisito cumple con los estándares ISO/IEC 25000 (RQA). La tubería está despejada para pasar a la fase de desarrollo."
    requests.post(comment_url, json={"body": success_msg}, headers=headers)
    
    print("Estado: Calidad Verificada. Etiqueta RQA-PASSED y comentario aplicados.")
>>>>>>> main
