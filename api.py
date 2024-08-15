from fastapi import FastAPI
from summary import get_summary
from scrapper import extract_text
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    url:HttpUrl
    word_limit:int

@app.post("/summarize-text")
async def get_url(request:Request):
    global summarized_text
    scrapped_text=extract_text(request.url)
    print(scrapped_text)
    if(request.word_limit==None):
        request.word_limit=151
    summarized_text=get_summary(scrapped_text,request.word_limit)
    print(summarized_text)
    return {"summary": summarized_text}
    