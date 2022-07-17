from typing import Union

from fastapi import FastAPI
from haystack.nodes import FARMReader, TransformersReader
from haystack.utils import print_answers
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline


app = FastAPI()

url = "search-auto-insurance-nbdvjfxbsyudd5yhpq3e4ic6bu.ap-south-1.es.amazonaws.com"
username = "tarunm"
password = "May#2022password"

document_store = OpenSearchDocumentStore(host=url,port=443, username=username, password=password, index="auto-insurance")
#retriever = BM25Retriever(document_store=document_store)

retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    max_seq_len_query=64,
    max_seq_len_passage=256,
    batch_size=16,
    use_gpu=True,
    embed_title=True,
    use_fast_tokenizers=True,
)

reader =FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

pipe = ExtractiveQAPipeline(reader=reader, retriever=retriever)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query")
async def get_answer(query: str):
    global pipe
    result = pipe.run(query=query)

    return result['answers'][0].answer 

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}