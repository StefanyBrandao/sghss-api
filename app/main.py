from fastapi import FastAPI
from .db import Base, engine
from .routers import auth, patients

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGHSS VidaPlus - API")

app.include_router(auth.router)
app.include_router(patients.router)

@app.get("/")
def health():
    return {"status": "ok"}