from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse


from qna_app.backend.src.apis.answers import answers_router
from qna_app.backend.src.apis.questions import question_router
from qna_app.backend.src.apis.comments import comments_router

app = APIRouter(prefix="/qna_app")

app.include_router(answers_router)
app.include_router(question_router)
app.include_router(comments_router)


@app.get("/static/default-icon.svg")
async def router_root():
    content = "<img src='/static/default-icon.svg'>"
    return HTMLResponse(content=content)


@app.get("/")
async def read_root():
    return RedirectResponse(url="http://127.0.0.1:8000/qna_app/frontend/out/index.html")
