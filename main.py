from fastapi import FastAPI, HTTPException
import gensim
from gensim.models import word2vec
from pydantic import BaseModel
import random

app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})

model_path = './content/model.bin'
model_ru = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)


class Similarity(BaseModel):
    similarity: float
    rank: int


class Association(BaseModel):
    similarity: float
    rank: int
    word: str


@app.get("/similarity/{w1}/{w2}", response_model=Similarity, tags=['similarity'])
async def get_words_similarity(w1: str, w2: str):
    return {
        "similarity": model_ru.similarity(w1, w2),
        "rank": 0 if w1 == w2 else model_ru.rank(w1, w2),
    }


@app.get("/{main_word}/associations", response_model=Association, tags=['associations'])
async def get_word_association(main_word: str, guessed_word: str = None, rank: int = None):
    if rank is not None:
        if rank == 0:
            return {
                "similarity": 1,
                "rank": 0,
                "word": main_word,
            }

        associated_word = model_ru.most_similar(main_word, topn=rank)[-1][0]

        return {
            "similarity": model_ru.similarity(main_word, associated_word),
            "rank": 0 if main_word == associated_word else model_ru.rank(main_word, associated_word),
            "word": associated_word,
        }

    if guessed_word is not None:
        return {
            "similarity": model_ru.similarity(main_word, guessed_word),
            "rank": model_ru.rank(main_word, guessed_word),
            "word": guessed_word,
        }

    raise HTTPException(status_code=400)


@app.get("/random", tags=['random'])
async def get_random_word():
    return random.sample(model_ru.index_to_key, 1)[0]
