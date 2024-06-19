# @author Mohan Sharma
# com/crack/snap/make/di.py
import sys
import os
from com.crack.snap.make.containers import Container
from com.crack.snap.make import services, routes, model, utils

container = Container()

# Set the environment based on user input
container.env.override(
	lambda: os.environ.get("APP_ENV", "dev")
)

# Wire the container to allow it to inject dependencies in all modules
container.wire(modules=[sys.modules[__name__], services, routes, model, utils])
