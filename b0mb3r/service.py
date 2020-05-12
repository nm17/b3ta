import inspect
import os
import sys
from typing import Dict, Union

from loguru import logger


@logger.catch
def load_services(directory: str) -> Dict[Union[int, str], list]:
    files = os.listdir(directory)
    sys.path.insert(0, directory)
    all_phone_codes: Dict[Union[int, str], list] = {}
    special_services = []

    for file in files:
        if file.endswith(".py") and file != "service.py":
            module = __import__(file.replace(".py", ""))
            for member in inspect.getmembers(module, inspect.isclass):
                if member[1].__module__ == module.__name__:
                    service = getattr(module, member[0])

                    if len(service.phone_codes) == 0:
                        special_services.append(service)

                    for phone_code in service.phone_codes:
                        if phone_code not in all_phone_codes:
                            all_phone_codes[phone_code] = []

                        all_phone_codes[phone_code].append(service)

    for special_service in special_services:
        for key, value in all_phone_codes.items():
            all_phone_codes[key].append(special_service)

    all_phone_codes["other"] = special_services

    logger.success("Services preparation complete")
    return all_phone_codes


services = load_services(
    "services"
)  # This function takes some time, so it is better to only run it once
