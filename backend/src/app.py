from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse


from qna.backend.src.routers.answers import answers_router
from qna.backend.src.routers.questions import questions_router
from qna.backend.src.routers.comments import comments_router

app = APIRouter(prefix="/qna")

app.include_router(answers_router)
app.include_router(questions_router)
app.include_router(comments_router)


@app.get("/static/default-icon.svg")
async def router_root():
    content = "<img src='/static/default-icon.svg'>"
    return HTMLResponse(content=content)


@app.get("/")
async def read_root():
    return RedirectResponse(url="http://127.0.0.1:8000/qna/frontend/out/index.html")
