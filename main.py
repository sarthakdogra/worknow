from fastapi import FastAPI
from router.user import router as user_router
from router.admin import router as admin_router
from router.worker import router as worker_router
from router.costumer import router as costumer_router
from database import engine, Base
import models.user  # Import models to ensure they are registered with Base.metadata

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(costumer_router)
app.include_router(admin_router)
app.include_router(worker_router)

@app.get("/")
def gethealth():
    return {
        "status":"working"
    }
