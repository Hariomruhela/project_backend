from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import auth, projects, admin
from routes.contact import router as contact_router


# =========================
# CREATE DATABASE TABLES
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Portfolio API",
    version="1.0.0"
)

# =========================
# CORS
# =========================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",

    # Frontend production URL
     "https://techquitoes.vercel.app",
     "https://techquitoes-protfolio.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("CORS CONFIG LOADED")

# =========================
# ROUTES
# =========================
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(admin.router)
app.include_router(contact_router, prefix="/api")
# =========================
# ROOT ROUTE
# =========================
@app.get("/")
def root():
    return {
        "message": "Portfolio API is running 🚀"
    }