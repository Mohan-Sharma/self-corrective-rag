# @author Mohan Sharma
import multiprocessing
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from com.crack.snap.make.di import container
from com.crack.snap.make.routes.app_routes import router as AppRoutes
from com.crack.snap.make.routes.chat_client_routes import \
	router as ChatClientRoutes


class SelfCorrectiveRagApp:
	
	def __init__(self) -> None:
		load_dotenv()
		self.app: FastAPI = FastAPI()
		self.settings = container.settings()
		self.configure_app()
	
	def configure_app(self) -> None:
		self.register_routes()
		self.register_templates()
	
	def register_routes(self) -> None:
		self.app.include_router(AppRoutes)
		self.app.include_router(ChatClientRoutes)

	def register_templates(self) -> None:
		base_path = Path(__file__).resolve().parent
		self.app.mount("/static", StaticFiles(directory=base_path / "static"), name="static")
	
	def run(self) -> None:
		uvicorn.run(self.app, host=self.settings.host, port=self.settings.port, log_level="debug" if self.settings.debug else "info")


def create_app():
	app_instance = SelfCorrectiveRagApp()
	return app_instance.app


# required by guvicorn to run the app
app = create_app()


# run the app directly
if __name__ == "__main__":
	app = SelfCorrectiveRagApp()
	app.run()

