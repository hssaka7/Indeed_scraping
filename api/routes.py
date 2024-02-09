from fastapi import FastAPI

import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {'code':'success', 'message':"Hello World!"}


if __name__ == "__main__":
    uvicorn.run('routes:app', host='127.0.0.1', port=8000, reload=True)
    print("API coming soon http://127.0.0.1:8000/")
