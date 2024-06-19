# @author Mohan Sharma
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends

from com.crack.snap.make.config import CommonSettings
from com.crack.snap.make.di import container
from com.crack.snap.make.model import UserMessage
from com.crack.snap.make.services import SelfCorrectiveRagService

router = APIRouter(prefix="/ai")


@router.get("/greetings")
@inject
async def greetings(config: CommonSettings = Depends(lambda: container.settings())):
	if config.debug:
		print(f"Running in port {config.port}")
	return "Hello from the chat client!"


@router.post("/generate", response_model=dict)
@inject
async def generate_response(user_message: UserMessage, service: SelfCorrectiveRagService = Depends(lambda: container.rag_service())):
	res = service.generate(user_message.message)
	return {"response": res}
