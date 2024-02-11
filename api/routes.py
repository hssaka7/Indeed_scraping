from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from typing import List

import uvicorn

from schema import Feed,Worker, Result, Feed_Pydantic, Worker_Pydantic,Result_Pydantic

app = FastAPI()

@app.get("/")
async def root():
    return {'code':'success', 'message':"Hello World!"}

@app.get("/feeds", response_model=List[Feed_Pydantic])
async def get_feeds():
    all_feed = Feed.all()
    return await Feed_Pydantic.from_queryset(all_feed)

@app.get("/feeds/{id}", response_model=Feed_Pydantic)
async def get_feed(id: int):
    f_id = Feed.get(id=id)
    return await Feed_Pydantic.from_queryset_single(f_id)

@app.get("/workers", response_model=List[Worker_Pydantic])
async def get_workers():
    all_worker = Worker.all()
    return await Worker_Pydantic.from_queryset(all_worker)

@app.get("/workers/{id}", response_model=Worker_Pydantic)
async def get_worker(id: str):
    w_id = Worker.get(id=id)
    return await Worker_Pydantic.from_queryset_single(w_id)

@app.get("/results/{worker_id}")
async def get_results(worker_id:str):
    all_result = Result.all()
    return await Result_Pydantic.from_queryset(all_result)

register_tortoise(
    app,
    db_url="sqlite://scrapers.db",
    modules={"models": ["schema"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run('routes:app', host='127.0.0.1', port=8000, reload=True)
