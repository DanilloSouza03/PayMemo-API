from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infra.bill_controller import router as bill_router
from src.infra.user_controller import router as user_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
def iniciarAPI():
    return "Route inicial..."


app.include_router(bill_router)
app.include_router(user_router)
