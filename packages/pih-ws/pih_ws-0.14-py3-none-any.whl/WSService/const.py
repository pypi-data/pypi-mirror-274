import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "WS"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.14"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Workstation service",
    host=HOST.NAME,
    commands=(
        "reboot",
        "shutdown",
        "send_message_to_user_or_workstation",
        "kill_process",
    ),
    use_standalone=True,
    standalone_name="ws",
    version=VERSION,
)
