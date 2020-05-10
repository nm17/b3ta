import inspect
import os
import sys
from types import ModuleType
from typing import Dict

from loguru import logger

from b0mb3r.services.service import Service


@logger.catch
def load_services(directory: str) -> Dict[ModuleType, Service]:
    files = os.listdir(directory)
    sys.path.insert(0, directory)
    service_objects: Dict[ModuleType, Service] = {}

    for file in files:
        if file.endswith(".py") and file != "service.py":
            module = __import__(file.replace(".py", ""))
            for member in inspect.getmembers(module, inspect.isclass):
                if member[1].__module__ == module.__name__:
                    service_objects[module] = member[0]

    logger.success("Services preparation complete")
    return service_objects


services = load_services(
    "services"
)  # Time elapsed by function is around 0.8 seconds, so it is better to only run it once
