from fastapi import FastAPI
from app.api.endpoints import user, post, comments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comments.router)

@app.get("/")
def welcome_page():
    return {"message": "Welcome to the Blog API"}
