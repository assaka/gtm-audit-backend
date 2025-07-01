from fastapi import FastAPI
from routes import gtm

app = FastAPI(
    title="AI GTM Audit",
    description="Audit websites and Google Tag Manager setup",
    version="1.0.0"
)

# ✅ This must come immediately after app is created
app.include_router(gtm.router, prefix="/gtm", tags=["GTM Audit"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI GTM Audit API!"}
