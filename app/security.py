from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = "TROQUE_ISS0_PARA_UMA_CHAVE_FORTE"
JWT_ALG = "HS256"
JWT_EXPIRE_MIN = 60

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MIN)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
