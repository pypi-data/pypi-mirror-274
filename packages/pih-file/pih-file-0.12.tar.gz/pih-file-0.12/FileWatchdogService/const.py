import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription


NAME: str = "FileWatchdog"

HOST = Hosts.BACKUP_WORKER

PACKAGES: tuple[str, ...] = ("watchdog",)

VERSION: str = "0.12"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="FileWatchdog service",
    host=HOST.NAME,
    commands=("listen_for_new_files",),
    version=VERSION,
    use_standalone=True,
    standalone_name="file",
    packages=PACKAGES,
)
