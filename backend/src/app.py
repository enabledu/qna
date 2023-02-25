from fastapi import APIRouter

from core.backend.src.database import init_db, create_client, close_client

from qna_app.backend.src.apis.answers import answers_router
from qna_app.backend.src.apis.questions import question_router

app = APIRouter()
app.include_router(answers_router,
                   prefix="/answers",
                   tags=["answers"])
app.include_router(question_router,
                   prefix="/questions",
                   tags=["questions"])


@app.on_event("startup")
async def on_startup():
    print("Startup...")
    await create_client()
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    print("Shutdown...")
    await close_client()
