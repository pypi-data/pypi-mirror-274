import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts
from pih.consts import CONST

NAME: str = "PolibaseAutomation"

VERSION: str = "0.14"

HOST = Hosts.POLIBASE

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Polibase automation service",
    host=HOST.NAME,
    python_executable_path=CONST.UNKNOWN_VALUE,
    run_from_system_account=True,
    standalone_name="plb_auto",
    use_standalone=True,
    version=VERSION,
)
