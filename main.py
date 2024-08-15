from model import model
import pandas as pd
import numpy as np
import pickle
from fastapi import FastAPI, Response
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
async def lifespan(app: FastAPI) -> None:
    with open(empath, "rb") as file:
        app.state.embeddings = np.array(list(pickle.load(file).values()))

    app.state.questions = pd.read_csv("data.csv")

    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"Status": "Online"}

@app.get("/q/{question}")
async def get_answer(question: str):

    q_em = model.encode(question, show_progress_bar=True)

    cs = q_em @ app.state.embeddings[:,0].T

    ids = np.argpartition(cs, -4)[-4:]

    ids = ids[np.argsort(cs[ids])][::-1]

    return {
        "answers": app.state.questions.loc[ids].to_dict('records'),
    }



@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=404)


if __name__ == "__main__":
    uvicorn.run(app)