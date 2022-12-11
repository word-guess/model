from fastapi import FastAPI
import gensim
from gensim.models import word2vec
from pydantic import BaseModel
import random

app = FastAPI()

model_path = './content/model.bin'
model_ru = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)


class Similarity(BaseModel):
    similarity: float
    rank: int


@app.get("/similarity/{w1}/{w2}", response_model=Similarity)
async def get_words_similarity(w1: str, w2: str):
    return {
        "similarity": model_ru.similarity(w1, w2),
        "rank": model_ru.rank(w1, w2),
    }


@app.get("/random")
async def get_random_word():
    return random.sample(model_ru.index_to_key, 1)[0]
