import hashlib
import secrets
import string

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash simple para ejemplo (usa SHA256, para producción usa bcrypt o similar)"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verifica si el hash de la contraseña coincide"""
        return PasswordManager.hash_password(password) == hashed

    @staticmethod
    def validate_password_strength(password: str):
        """Valida fuerza mínima de la contraseña"""
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe tener al menos un número"
        if not any(c.isalpha() for c in password):
            return False, "La contraseña debe tener al menos una letra"
        return True, "OK"

    @staticmethod
    def generate_secure_password(length=12) -> str:
        """Genera una contraseña segura aleatoria"""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(chars) for _ in range(length))