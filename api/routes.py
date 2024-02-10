from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from typing import List

import uvicorn

from schema import Feed,Result_Pydantic_List, Feed_Pydantic_List, Feed_Pydantic

app = FastAPI()

@app.get("/")
async def root():
    return {'code':'success', 'message':"Hello World!"}

@app.get("/feeds", response_model=List[Feed_Pydantic])
async def get_feeds():
    all_feed = Feed.all()
    print(all_feed)
    return await Feed_Pydantic.from_queryset(Feed.all())

register_tortoise(
    app,
    db_url="sqlite://scrapers.db",
    modules={"models": ["schema"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run('routes:app', host='127.0.0.1', port=8000, reload=True)
    print("API coming soon http://127.0.0.1:8000/")
