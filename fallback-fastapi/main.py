from typing import Union

from fastapi import FastAPI
from haystack.nodes import FARMReader, TransformersReader
from haystack.utils import print_answers
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline


app = FastAPI()

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="auto_insurance")

# retriever = DensePassageRetriever(
#     document_store=document_store,
#     query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
#     passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
#     max_seq_len_query=64,
#     max_seq_len_passage=256,
#     batch_size=16,
#     use_gpu=True,
#     embed_title=True,
#     use_fast_tokenizers=True,
# )
retriever = BM25Retriever(document_store=document_store)
#reader = FARMReader(model_name_or_path="twmkn9/distilbert-base-uncased-squad2", use_gpu=-1)
reader = FARMReader(model_name_or_path="deepset/tinyroberta-squad2", use_gpu=False)

pipe = ExtractiveQAPipeline(reader=reader, retriever=retriever)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query")
async def get_answer(query: str):
    result = pipe.run(query=query)
    out=[]
    out.append("answer :"+result['answers'][0].answer)
    out.append("context :"+ result['answers'][0].context)
    return out 

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}