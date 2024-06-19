# @author Mohan Sharma
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dependency_injector.wiring import inject
from com.crack.snap.make.config import CommonSettings
from com.crack.snap.make.di import container

router = APIRouter()

templates = Jinja2Templates(directory="com/crack/snap/make/templates")


@router.get("/", response_class=HTMLResponse)
@inject
async def index(request: Request, config: CommonSettings = Depends(lambda: container.settings())):
	return templates.TemplateResponse("index.html", {
		"request": request,  # this is required by Jinja2
		"debug_mode": "on" if config.debug else "off"
	})
