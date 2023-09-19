import os

import uvicorn
from fastapi import FastAPI

from database import Base, engine

app = FastAPI()

@app.on_event("startup")
async def setting_scheduler():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", 8000), reload=True)