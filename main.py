from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import auth, projects

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(projects.router)


@app.get("/")
def root():
    return {"message": "Portfolio API is running 🚀"}