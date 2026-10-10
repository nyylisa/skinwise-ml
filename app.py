from gradio import Server
from pydantic import BaseModel
from setfit import SetFitModel
from fastapi.middleware.cors import CORSMiddleware

app = Server()

# Added CORS just in case
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your model from Hugging Face Hub (not a local folder)
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


app.launch()
