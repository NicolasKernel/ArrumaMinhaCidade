import re
import requests


def validate_email(email):
        API_KEY = '62bb42f1e61c42e09bead379af4d74f1'
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}"
        try:
            response = requests.get(url)
            data = response.json()
            # Checa se o e-mail é válido e existe
            return data.get("deliverability") == "DELIVERABLE"
        except Exception as e:
            print(f"Erro ao validar e-mail via API: {e}")
            return False


def validate_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:
        return False  # Rejeita CPFs com todos os dígitos iguais

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if int(cpf[i]) != digito:
            return False
    return True


def validate_cep(cep): # Validação de Cep utilizando a API ViaCEP 
    cep = re.sub(r'\D', '', cep)
    if not re.match(r'^\d{8}$', cep):
        return False
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        data = response.json()
        print(f"CEP {cep} encontrado: {data.get('logradouro', 'não disponível')}, {data.get('bairro', 'não disponível')}, {data.get('localidade', 'não disponível')}, {data.get('uf', 'não disponível')}")
        if 'erro' in data:
            print(f"CEP {cep} não encontrado.")
            return False
        return True
    except Exception:
        return False