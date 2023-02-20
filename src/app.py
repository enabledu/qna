from fastapi import FastAPI
from src.db import init_db, create_client, close_client
from src.answers import answers_router
from src.questions import question_router
from src.comments import comments_router
from src.schemas import UserCreate, UserRead, UserUpdate
from src.users import auth_backend, fastapi_users

app = FastAPI()

app.include_router(
    answers_router,
    prefix="/answers",
    tags=["answers"]
)
app.include_router(
    comments_router,
    prefix="/comments",
    tags=["comments"]
)
app.include_router(
    question_router,
    prefix="/questions",
    tags=["questions"]
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


# @app.get("/authenticated-route")
# async def authenticated_route(user: User = Depends(current_active_user)):
#    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    print("Startup...")
    await create_client()
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    print("Shutdown...")
    await close_client()
