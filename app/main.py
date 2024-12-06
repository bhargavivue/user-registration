from fastapi import FastAPI
from routers import user_router
from  core.database import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include the user router
app.include_router(user_router.router)
