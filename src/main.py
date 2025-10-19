from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infra.bill_controller import router as bill_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(bill_router)
