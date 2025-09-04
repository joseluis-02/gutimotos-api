# Firebase Admin
from firebase_admin import auth

# Decodificar el token de Google
def verify_google_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token)
        #print("Token verificado correctamente:", decoded)
        return {
            "auth_uid": decoded["uid"],
            "email": decoded.get("email"),
            "auth_provider" : decoded.get("firebase", {}).get("sign_in_provider"),
            "email_verified" : decoded.get('email_verified')
        }
    except Exception as e:
        raise ValueError(f"Token inválido o expirado: {e}")
