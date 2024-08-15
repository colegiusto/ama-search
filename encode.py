from sentence_transformers import SentenceTransformer
import pandas as pd
import pickle
from tqdm import tqdm


data_path = "data.csv"
def encode(df: pd.DataFrame):
    from model import model
    
    questions: pd.Series = df["Question"]
    answers: pd.Series = df["Answer"]

    questions = model.encode(questions, show_progress_bar=True)
    answers = model.encode(answers, show_progress_bar=True, batch_size=1)

    embeddings = {}
    for i,(q,a) in tqdm(enumerate(zip(questions, answers))):
        embeddings[i] = (q, a)

    with open("embeddings.pickle", "wb+") as file:
        pickle.dump(embeddings, file)

def load_data():
    df = pd.read_csv(data_path)
    return df

if __name__ == "__main__":
    encode(load_data())