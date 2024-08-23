from model import model
import pandas as pd
import numpy as np
import pickle
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
from contextlib import asynccontextmanager



empath = "embeddings.pickle"





def main():
    with open(empath, "rb") as file:
        data = pickle.load(file)

    df = pd.read_csv("data.csv")

    question =  input("Question: ")

    question_embedding = model.encode(question, show_progress_bar=True)

    cq = -1
    qid = 0
    for i, d in data.items():
        q = d[0]
        c = np.dot(q, question_embedding)/(np.linalg.norm(q)*np.linalg.norm(question_embedding))
        if c > cq:
            cq = c
            qid = i
        
    print(df["Question"][qid])

embeddings = {}
questions = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    with open(empath, "rb") as file:
        app.state.embeddings = np.array(list(pickle.load(file).values()))
    
    app.state.embeddings = app.state.embeddings/np.linalg.norm(app.state.embeddings, axis=2, keepdims=True)

    app.state.questions = pd.read_csv("data.csv")

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "amasearch.dwab.dev"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://amasearch.dwab.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Status": "Online"}

@app.get("/ask/")
async def get_answer(q: str, limit: int = 5):

    q_em = model.encode(q)

    cs = q_em @ app.state.embeddings[:,0].T

    ids = np.argpartition(cs, -limit)[-limit:]

    ids = ids[np.argsort(cs[ids])][::-1]

    return {
        "results": app.state.questions.loc[ids].to_dict('records'),
    }



@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=404)


if __name__ == "__main__":
    uvicorn.run(app)