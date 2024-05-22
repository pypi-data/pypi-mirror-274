import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts

NAME: str = "Gateway"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.13"

PACKAGES: tuple[str, ...] = ("fastapi", "uvicorn")

ALISA_TIMEOUT: int = 4100

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Whatsapp message and Alisa command gateway service",
    host=HOST.NAME,
    host_changeable=False,
    version=VERSION,
    standalone_name="gateway",
    use_standalone=True,
    packages=PACKAGES
)
