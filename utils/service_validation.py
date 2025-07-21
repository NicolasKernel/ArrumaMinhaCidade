import json
import os

def is_duplicate_service(cep, service_type, json_file):
    """
    Verifica se já existe um serviço com o mesmo CEP e tipo no arquivo JSON.
    Retorna True se encontrar duplicata, False caso contrário.
    """
    if not os.path.exists(json_file):
        return False

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            all_services = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for service in all_services.values():
        if service.get('cep') == cep and service.get('type') == service_type:
            return True
    return False