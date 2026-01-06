from fastapi import FastAPI

app = FastAPI(title="Enterprise Document Intelligence")

@app.get("/health")
def health():
    return {"status": "ok"}