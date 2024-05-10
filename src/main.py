from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router_jwt import router as auth_router
from auth.user_router import router as user_router
from tasks.projects_router import router as projects_router
from tasks.tasks_router import router as tasks_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_router, prefix="/api")
app.include_router(router=user_router, prefix="/api")
app.include_router(router=projects_router, prefix="/api")
app.include_router(router=tasks_router, prefix="/api")

@app.get("/")
def get_hello():
    return "Hello world!"

