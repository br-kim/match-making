import os

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from routers import index_router, match_router, user_router
from database import Base, engine
from schedule import game_matching_1vs1, game_matching_2vs2

app = FastAPI()
app.include_router(index_router)
app.include_router(match_router)
app.include_router(user_router)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)
    scheduler = BackgroundScheduler()
    scheduler.add_job(game_matching_1vs1, "interval", seconds=10)
    scheduler.add_job(game_matching_2vs2, "interval", seconds=10)

    scheduler.start()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", 8000), reload=True)
