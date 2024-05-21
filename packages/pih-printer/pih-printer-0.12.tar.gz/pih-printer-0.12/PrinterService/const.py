import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts

from enum import Enum

NAME: str = "Printer"

HOST = Hosts.WS255

VERSION: str = "0.12"

PACKAGES: tuple[str, ...] = (
    "pyasn1==0.4.8",
    "pycryptodomex==3.15.0",
    "pysmi==0.3.4",
    "pysnmp",
)

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Printer service",
    host=HOST.NAME,
    commands=("printers_report", "printer_snmp_call"),
    use_standalone=True,
    standalone_name="printer",
    packages=PACKAGES,
    version=VERSION,
)


class PrinterCommands(Enum):
    REPORT = "report"
    STATUS = "status"
