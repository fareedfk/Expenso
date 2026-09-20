from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from apps.api.core.database import engine, Base
from apps.api.domain.auth.router import router as auth_router
from apps.api.domain.transactions.router import router as tx_router
from apps.api.domain.categories.router import router as cat_router
from apps.api.domain.payment_methods.router import router as pm_router
from apps.api.domain.budgets.router import router as budget_router
from apps.api.domain.analytics.router import router as analytics_router
from apps.api.domain.recurring.router import router as recurring_router
from apps.api.domain.export.router import router as export_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expenso API",
    description="Enterprise Clean Architecture Backend for Expenso",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tx_router)
app.include_router(cat_router)
app.include_router(pm_router)
app.include_router(budget_router)
app.include_router(analytics_router)
app.include_router(recurring_router)
app.include_router(export_router)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Expenso API Monorepo", "version": "2.0.0"}

WEB_PUBLIC_DIR = Path(__file__).resolve().parent.parent / "web" / "public"
if WEB_PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=WEB_PUBLIC_DIR), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(WEB_PUBLIC_DIR / "index.html")
