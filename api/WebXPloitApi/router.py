# cython: language_level=3


import pyximport

pyximport.install()

import asyncio
import uvicorn
import src.utils.specifics.url_manager as URLManager
from fastapi import FastAPI, status
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from src.utils.specifics.once_make_env import OnceMakeEnvironment


app = FastAPI()
url_manager = URLManager.URLManager()


async def init_orm():
    await Tortoise.init(
        db_url="sqlite://./sql/db.sqlite3", modules={"models": ["src.utils.specifics.url_manager"]}
    )
    await Tortoise.generate_schemas()


@app.on_event("startup")
async def on_startup():
    await init_orm()
    asyncio.create_task(url_manager.process_urls())


@app.on_event("shutdown")
async def on_shutdown():
    await Tortoise.close_connections()


register_tortoise(
    app,
    db_url="sqlite://./sql/db.sqlite3",
    modules={"models": ["src.utils.specifics.url_manager"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.post("/url/post", status_code=status.HTTP_201_CREATED)
async def push_git_url(url_request: URLManager.UrlRequest):
    return await url_manager.url_adding_controller(url_request)


@app.get("/url/get/{limit}", status_code=status.HTTP_200_OK)
@app.get("/url/get", status_code=status.HTTP_200_OK)
async def fetch_git_urls(limit: int = None):
    return await url_manager.fetch_urls(limit)


@app.delete("/url/delete", status_code=status.HTTP_200_OK)
async def delete_url(delete_request: URLManager.UrlRequest):
    return await url_manager.url_deleting_controller(delete_request)


@app.delete("/url/delete/all", status_code=status.HTTP_200_OK)
async def delete_url():
    return await URLManager.DbUrl.all().delete()


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


OnceMakeEnvironment()
# uvicorn.run(app, host="127.0.0.1", port=8000)
