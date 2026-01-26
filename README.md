# SGHSS VidaPlus - Back-end API

*Descrição
Este projeto consiste no desenvolvimento de uma API REST para o Sistema de Gestão Hospitalar e de Serviços de Saúde (SGHSS) da instituição VidaPlus.  
A aplicação foi desenvolvida como parte do trabalho acadêmico da trilha Back-end, utilizando Python e FastAPI.

O sistema contempla autenticação de usuários, cadastro de pacientes, agendamento de consultas e trilha de auditoria, respeitando princípios básicos da LGPD.

---

*Tecnologias Utilizadas
- Python 3.12
- FastAPI
- SQLAlchemy 
- SQLite 
- JSON Web Token 
- Passlib / bcrypt
- Uvicorn
- Swagger UI

---

*Arquitetura do Projeto

O sistema segue uma arquitetura baseada em API REST, organizada em módulos:

sghss-api/
│
├── app/
│  ├── _init_.py
│  ├── audit.py  
│  ├── db.py
│  ├── main.py 
│  ├── models.py 
│  ├── schemas.py   
│  ├── security.py
│  │
│  └────── routers/
│           ├── _init_.py
│           ├── admissions.py
│           ├── appointments.py
│           ├── auth.py  
│           ├── beds.py 
│           ├── medical_records.py
│           ├── patients.py
│           ├── prescriptions.py
│           ├── professionals.py
│           ├── reports.py
│           └── teleconsults.py
│
├── _init_.py
├── README.md
├── requirements.txt
└── sghss.db


---

*Como Executar o Projeto
```bash
git clone https://github.com/StefanyBrandao/sghss-api.git
cd sghss-api



