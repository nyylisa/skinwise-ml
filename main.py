import os
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from setfit import SetFitModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy-loaded model
_model = None
_model_lock = threading.Lock()


def get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                print("Loading SetFit model from HF Hub...")
                _model = SetFitModel.from_pretrained("nyylisaa/skinwise-setfit-model")
                print("Model loaded.")
    return _model


class ClassifyRequest(BaseModel):
    ingredients: list[str]


@app.post("/classify")
def classify(req: ClassifyRequest):
    if not req.ingredients:
        return {"results": []}
    model = get_model()
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