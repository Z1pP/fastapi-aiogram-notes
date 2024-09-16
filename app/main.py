import uvicorn
from fastapi import FastAPI

from app.api.v1.user import router as user_router
from app.api.v1.note import router as note_router

app = FastAPI(docs_url="/api")
app.include_router(user_router)
app.include_router(note_router)


if __name__=="__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port="8000", reload=True)
    except KeyboardInterrupt:
        exit()