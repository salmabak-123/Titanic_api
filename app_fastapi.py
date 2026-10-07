from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from core import Passenger, predict

app = FastAPI()


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs")


@app.post("/make_predictions")
async def make_predictions(passenger: Passenger):
    return predict(passenger)


if __name__ == "__main__":
    uvicorn.run("app_fastapi:app", host="0.0.0.0", port=8081, reload=True)