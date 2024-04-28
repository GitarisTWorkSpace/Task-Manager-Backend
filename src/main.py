from fastapi import FastAPI
from auth.router_jwt import router as auth_router
from auth.router import router as me_router

app = FastAPI()

app.include_router(router=auth_router, prefix="/api")
app.include_router(router=me_router, prefix="/api")

@app.get("/")
def get_hello():
    return "Hello world!"

