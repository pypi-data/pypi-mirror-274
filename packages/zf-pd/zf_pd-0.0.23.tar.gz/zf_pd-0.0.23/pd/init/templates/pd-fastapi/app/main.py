from sys import stderr
from sys import stdout

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .routers import home

logger.remove(0)
logger.add(stdout, level="DEBUG")
logger.add(stderr, level="ERROR")
logger.add("logs/app.log", level="DEBUG", rotation="1 day", retention="1 week")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home.router)

origins = [
    # Replace this with your domain
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
