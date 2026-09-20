import uvicorn
from apps.api.core.database import init_database, Base

def main():
    print("==================================================")
    print("  Expenso Monorepo — Personal Expense Tracker")
    print("  Starting server on http://localhost:8000")
    print("==================================================")
    
    eng = init_database()
    Base.metadata.create_all(bind=eng)
    print("[OK] Database verified & tables created.")

    uvicorn.run(
        "apps.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
