from fastapi import FastAPI
from app.api.endpoints import user, post, comments

app = FastAPI(title="Blog API")

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comments.router)

@app.get("/")
def welcome_page():
    return {"message": "Welcome to the Blog API"}
