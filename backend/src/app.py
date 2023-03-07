from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse

from enabled.backend.src.database import init_db, create_client, close_client

from qna_app.backend.src.apis.answers import answers_router
from qna_app.backend.src.apis.questions import question_router
from qna_app.backend.src.apis.comments import comments_router

app = APIRouter(tags=["qna"], prefix="/qna_app")

app.include_router(answers_router)
app.include_router(question_router)
app.include_router(comments_router)


@app.on_event("startup")
async def on_startup():
    print("Startup...")
    await create_client()
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    print("Shutdown...")
    await close_client()


@app.get("/static/default-icon.svg")
async def router_root():
    content = "<img src='/static/default-icon.svg'>"
    return HTMLResponse(content=content)


@app.get("/")
async def read_root():
    return FileResponse("qna_app/frontend/build/index.html")