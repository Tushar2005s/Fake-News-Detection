from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import requests
from bs4 import BeautifulSoup
from googlesearch import search


model_path = "D:/Fake News Detector/fake_news_model.pkl"
vectorizer_path = "D:/Fake News Detector/vectorizer.pkl"

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


def get_news_sources(query):
    search_results = list(search(query, num_results=5))  
    sources = {}
    for url in search_results:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            text = ' '.join([p.text for p in soup.find_all('p')])
            sources[url] = text[:500]  
        except:
            continue
    return sources

@app.get("/predict/")
async def predict_news(news_text: str):
    if not news_text:
        raise HTTPException(status_code=400, detail="News text is required")

    
    transformed_text = vectorizer.transform([news_text])
    prediction = model.predict(transformed_text)[0]

    
    sources = get_news_sources(news_text)

    return {"prediction": prediction, "sources": sources}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
