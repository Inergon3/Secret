import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.secret import router as secret_router

app = FastAPI()

origins = ["http://localhost:8000",
           ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(secret_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host= "0.0.0.0", port=8000, reload=True)
