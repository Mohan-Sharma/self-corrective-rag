# @author Mohan Sharma
from pydantic import BaseModel


class UserMessage(BaseModel):
	message: str
