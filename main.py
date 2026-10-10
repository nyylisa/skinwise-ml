from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from setfit import SetFitModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Vercel, localhost, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model = SetFitModel.from_pretrained("skinwise-setfit-model")


class ClassifyRequest(BaseModel):
    ingredients: list[str]


@app.post("/classify")
def classify(req: ClassifyRequest):
    if not req.ingredients:
        return {"results": []}

    preds = model(req.ingredients)
    results = [
        {"ingredient": ing, "category": cat}
        for ing, cat in zip(req.ingredients, preds)
    ]
    return {"results": results}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)