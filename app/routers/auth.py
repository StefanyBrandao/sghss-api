from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..schemas import UserCreate, TokenOut
from ..security import hash_password, verify_password, create_token
from ..audit import log_action

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=dict)
def signup(data: UserCreate, request: Request, db: Session = Depends(get_db)):

    # 1. Verifica se o e-mail já existe
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado")

    # 2. Limpa a senha
    senha_limpa = str(data.senha).strip()

    # 3. Valida tamanho da senha (bcrypt)
    if len(senha_limpa.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Senha muito longa (máx. 72 bytes)"
        )

    # 4. Cria usuário
    user = User(
        nome=data.nome,
        email=data.email,
        senha_hash=hash_password(senha_limpa),
        role="PROFISSIONAL"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    log_action(
        db,
        user.id,
        "SIGNUP",
        "users",
        user.id,
        request.client.host if request.client else None
    )

    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "role": user.role
    }

@router.post("/login", response_model=TokenOut)
def login(email: str, senha: str, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(senha, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_token(user.id, user.role)
    log_action(db, user.id, "LOGIN", "users", user.id, request.client.host if request.client else None)
    return {"token": token}
