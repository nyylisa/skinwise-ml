from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from setfit import SetFitModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = SetFitModel.from_pretrained("nyylisaa/skinwise-setfit-model")


class ClassifyRequest(BaseModel):
    ingredients: list[str]


@app.post("/classify")
def classify(req: ClassifyRequest):
    if not req.ingredients:
        return {"results": []}
    preds = model(req.ingredients)
    return {
        "results": [
            {"ingredient": ing, "category": cat}
            for ing, cat in zip(req.ingredients, preds)
        ]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)