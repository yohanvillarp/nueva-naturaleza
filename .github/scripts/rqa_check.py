import os
import requests

# Configuración de entorno
body = os.getenv("ISSUE_BODY", "").lower()
issue_number = os.getenv("ISSUE_NUMBER")
repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Lógica de Validación (Ingeniería de Requisitos - ISO 25000)
keywords = ["como", "quiero", "para"]
ambiguous_terms = ["rápido", "fácil", "bien", "mejor", "intuitivo", "eficiente"]

has_structure = all(word in body for word in keywords)
is_ambiguous = any(term in body for term in ambiguous_terms)
# Requisito válido si tiene estructura y no tiene términos ambiguos
is_valid = has_structure and not is_ambiguous

# URLs de la API de GitHub
label_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"

def safe_delete_label(label_name):
    """Evita errores 404 si la etiqueta no existe en el issue."""
    requests.delete(f"{label_url}/{label_name}", headers=headers)

if not is_valid:
    # 1. Limpieza de estados anteriores
    safe_delete_label("RQA-PASSED")
    
    # 2. Aplicación de etiquetas de error
    requests.post(label_url, json={"labels": ["RQA-FAILED", "AMBIGUOUS"]}, headers=headers)
    
    # 3. Feedback de Diagnóstico
    error_msg = (
        "🚨 **DIAGNÓSTICO DEL SISTEMA: INFRACCIÓN DE ESTÁNDAR [ERR-01]**\n\n"
        "> **PIPELINE BLOQUEADO.** El requisito no cumple con los criterios de calidad estrictos.\n\n"
        "**Análisis de Fallo:**\n"
        "- **Estructura:** Asegúrate de usar la sintaxis `Como [Rol], quiero [Acción], para [Beneficio]`.\n"
        "- **Métricas:** Se detectaron términos subjetivos. Evita palabras como 'rápido' o 'fácil'. Reemplázalas por métricas exactas.\n\n"
        "_Re-evaluación estricta requerida._"
    )
    requests.post(comment_url, json={"body": error_msg}, headers=headers)
    print("Estado: Calidad Insuficiente. Pipeline bloqueado.")

else:
    # 1. Limpieza de etiquetas de error anteriores
    safe_delete_label("RQA-FAILED")
    safe_delete_label("AMBIGUOUS")
    
    # 2. Aplicación de etiqueta de éxito
    requests.post(label_url, json={"labels": ["RQA-PASSED"]}, headers=headers)
    
    # 3. Feedback de Validación Exitosa
    success_msg = (
        "🟩 **SISTEMA DESPEJADO: STATUS OK**\n\n"
        "✅ **CALIDAD VERIFICADA.**\n"
        "Este requisito cumple con los estándares **ISO/IEC 25000 (RQA)**. "
        "La tubería está despejada para pasar a la fase de desarrollo."
    )
    requests.post(comment_url, json={"body": success_msg}, headers=headers)
    print("Estado: Calidad Verificada. Tubería despejada.")
