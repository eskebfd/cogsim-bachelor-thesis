from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(title="CogSim API")


app.include_router(router)


@app.get("/")
def read_root():

    return {
        "message": "CogSim API is running"
    }
