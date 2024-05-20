from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from loguru import logger
from starlette.requests import Request
from starlette.responses import HTMLResponse

from ..apis import example
from ..model import Example

router = APIRouter(
    prefix="",
    tags=["home"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    m: Example = Example(msg="Hello World")
    d = example(e=m)
    logger.debug(f"API call returned data: {d}")
    return templates.TemplateResponse("index.html", {"request": request, "data": d})
