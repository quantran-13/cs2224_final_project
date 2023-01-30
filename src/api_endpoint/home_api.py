import logging

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.const.global_map import RESOURCE_MAP
from src.utils.helpers import openfile


app = RESOURCE_MAP["fastapi_app"]
app_logger = logging.getLogger("app_logger")


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("home.html", {"request": request, "data": data})
