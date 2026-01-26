from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = "alunouninter4499602@"
JWT_ALG = "HS256"
JWT_EXPIRE_MIN = 60

def hash_password(password: str) -> str:
    senha = str(password).strip()
    senha = senha.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(senha)

def verify_password(password: str, hashed: str) -> bool:
    senha = str(password).strip()
    senha = senha.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(senha, hashed)

def create_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MIN)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
