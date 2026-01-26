from fastapi import FastAPI
from .db import Base, engine
from .routers import auth, patients
from app.routers import professionals


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGHSS VidaPlus - API", debug=True)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(professionals.router)


@app.get("/")
def health():
    return {"status": "ok"}