from fastapi import FastAPI
import gensim
from gensim.models import word2vec

app = FastAPI()

model_path = './content/model.bin'
model_ru = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)


@app.get("/most_similar/{word}", response_model=list[tuple[str, int]])
async def root(word: str, count: int):
    return model_ru.most_similar(positive=[word], topn=count)


@app.get("/similarity/{w1}/{w2}", response_model=float)
async def say_hello(w1: str, w2: str):
    return model_ru.similarity(w1, w2)
