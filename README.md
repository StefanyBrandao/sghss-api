# SGHSS VidaPlus - Back-end API

## 📌 Descrição
Este projeto consiste no desenvolvimento de uma API REST para o Sistema de Gestão Hospitalar e de Serviços de Saúde (SGHSS) da instituição VidaPlus.  
A aplicação foi desenvolvida como parte do trabalho acadêmico da trilha Back-end, utilizando Python e FastAPI.

O sistema contempla autenticação de usuários, cadastro de pacientes, agendamento de consultas e trilha de auditoria, respeitando princípios básicos da LGPD.

---

## 🛠️ Tecnologias Utilizadas
- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- JWT (Autenticação)
- Pydantic

---

## 📂 Estrutura do Projeto
sghss-api/
│
├── app/
│ ├── main.py
│ ├── db.py
│ ├── models.py
│ ├── schemas.py
│ ├── security.py
│ ├── audit.py
│ │
│ └── routers/
│ ├── auth.py
│ ├── patients.py
│ └── appointments.py
│
├── requirements.txt
└── README.md


---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/sghss-api.git
cd sghss-api

