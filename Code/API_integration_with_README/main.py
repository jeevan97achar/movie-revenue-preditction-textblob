from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from textblob import TextBlob
from joblib import load
import pandas as pd
from sklearn.preprocessing import StandardScaler
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

def analyze_sentiment(text):
  return TextBlob(text).sentiment.polarity

model = load("random_forest_model.pkl")

scaler = StandardScaler()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
  name: str
  price: float
  is_offer: bool = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
def process_data(data: dict):
  df = pd.DataFrame([data])
  df["overview_sentiment"] = df["overview"].apply(analyze_sentiment)
  df["keyword_sentiment"] = df["keywords"].apply(lambda x: analyze_sentiment(' '.join(x)))
  df = df.drop(["overview", "keywords"], axis=1)
  revenue_prediction = model.predict(df)
  return {"message": "Data processed", "revenue": revenue_prediction.tolist()[0]}