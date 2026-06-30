from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Smart Shopping Agent")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Smart Shopping Agent is running 🚀"}
