from fastapi import FastAPI

from .store import ModelStore

app = FastAPI()


class MetricsMiddleware:
    pass


def load_model(name: str) -> str:
    return ModelStore.load(name)


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/predict")
def predict(payload: dict) -> dict:
    model = load_model("champion")
    return {"model": model}
