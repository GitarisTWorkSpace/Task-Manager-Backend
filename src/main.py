from fastapi import FastAPI
from auth.route import router as auth_router

app = FastAPI()

app.include_router(router=auth_router)

@app.get("/")
def get_hello():
    return "Hello world!"

