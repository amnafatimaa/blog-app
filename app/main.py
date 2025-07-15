from fastapi import FastAPI
from app.api.endpoints import user, post

app = FastAPI(title="Blog API")

app.include_router(user.router)
app.include_router(post.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}