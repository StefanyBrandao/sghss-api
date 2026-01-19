from sqlalchemy.orm import Session
from .models import AuditLog

def log_action(db: Session, user_id: int, acao: str, entidade: str, entidade_id: int | None, ip: str | None):
    db.add(AuditLog(user_id=user_id, acao=acao, entidade=entidade, entidade_id=entidade_id, ip=ip))
    db.commit()
