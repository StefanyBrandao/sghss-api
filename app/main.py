from fastapi import FastAPI
from app.db import Base, engine


from app.routers import (
    auth,
    patients,
    professionals,
    appointments,
    medical_records,
    prescriptions,
    teleconsults,
    beds,
    admissions,
    reports,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGHSS VidaPlus - API", debug=True)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(professionals.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)
app.include_router(prescriptions.router)
app.include_router(teleconsults.router)
app.include_router(beds.router)
app.include_router(admissions.router)
app.include_router(reports.router)

@app.get("/")
def health():
    return {"status": "ok"}
