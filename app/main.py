import uvicorn
from fastapi import FastAPI

from app.api.v1 import router as api_router

app = FastAPI(docs_url="/api", openapi_prefix="/api/v1")
app.include_router(api_router)


if __name__=="__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port="8000", reload=True)
    except KeyboardInterrupt:
        exit()