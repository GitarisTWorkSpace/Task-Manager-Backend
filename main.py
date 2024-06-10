from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from api.auth.auth_router import auth_router
from api.user.user_router import user_router
from api.tasks.task_router import task_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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
app.include_router(router=task_router, prefix="/api")

@app.get("/")
def get_hello():
    return "Hello world!"


@app.get('/api/json_tea')
async def tea2(request: Request):
    rnd_pic = 'logo512.png'
    return FileResponse(rnd_pic)