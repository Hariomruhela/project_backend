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

# this coment for test purpose
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", 
        "http://127.0.0.1:3000",],      # or ["*"] for development
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