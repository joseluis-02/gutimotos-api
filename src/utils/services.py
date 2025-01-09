import requests
from decouple import config

def fetch_validate_and_create_invoice(token:str ,payload={}):
    try:
        response = requests.post(
            f"{config('BASE_URL_FACTUS')}/v1/bills/validate",
            json=payload,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise Exception(f"Error al llamar a la API: {str(e)}")
    
def fetch_login(payload={}):
    try:
        response = requests.post(
            f"{config('BASE_URL_FACTUS')}/oauth/token",
            json=payload,
            headers={
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise Exception(f"Error al llamar a la API: {str(e)}")
    
def fetch_invoices(token:str):
    try:
        print(token)
        response = requests.get(
            f"{config('BASE_URL_FACTUS')}/v1/bills",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
            params={
                'page': 1,
            }
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise Exception(f"Error al llamar a la API: {str(e)}")