from dataclasses import dataclass

import ipih
from pih import A
from PrinterService.const import PrinterCommands
from pih.collections import PrinterADInformation

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1905


class SNMPObject:

    def __init__(self, name: str | None, ip: str, port: int = A.CT.PORT.SNMP, community: str = "public",):
        self.name = name or ip
        self.ip = ip
        self.port = port
        self.community = community

    def get_snmp(self, oid: str):
        if self.name != -404:
            ip = self.ip
            port = self.port
            community = self.community
            cmdGen = cmdgen.CommandGenerator()
            errorIndication, errorStatus, _, varBinds = cmdGen.getCmd(
                # cmdgen.CommunityData(community, mpModel=0),
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((ip, port)),
                oid,
            )

            # Check for errors and print out results
            if errorIndication:
                if self.name == -401 and "timeout" in str(errorIndication):
                    return -404
                else:
                    return -1
            else:
                if errorStatus:
                    return -1
                else:
                    for _, value in varBinds:
                        if (
                            value == ""
                            or value == None
                            or isinstance(value, rfc1905.NoSuchInstance)
                            or isinstance(value, rfc1905.NoSuchObject)
                        ):
                            value = "-1"
                        value = str(value)
                        if value.isdigit() or self.isNegative(value):
                            return int(value)
                        return value
        else:
            return -404


@dataclass
class PrinterInformation:
    driverName: str | None = None
    adminDescription: str | None = None
    description: str | None = None
    portName: str | None = None
    serverName: str | None = None
    name: str | None = None
    variant: str | None = None


class Printer(SNMPObject):
    oid_printerName = "1.3.6.1.2.1.1.5.0"
    oid_printerModel = "1.3.6.1.2.1.25.3.2.1.3.1"
    oid_printerMeta = "1.3.6.1.2.1.1.1.0"
    # alternativ 1.3.6.1.4.1.2699.1.2.1.2.1.1.3.1
    # alternativ2 1.3.6.1.2.1.1.1.0
    oid_printerSerial = "1.3.6.1.2.1.43.5.1.1.17.1"
    # alternativ SN: 1.3.6.1.4.1.253.8.53.3.2.1.3.1

    oid_printsOverall = "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.1"
    oid_printsColor = "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33"
    oid_printsMonochrome = "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34"

    oid_fuserType = "1.3.6.1.2.1.43.11.1.1.6.1.9"
    oid_fuserCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.9"
    oid_fuserRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.9"

    oid_wasteType = "1.3.6.1.2.1.43.11.1.1.6.1.10"
    oid_wasteCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.10"
    oid_wasteRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.10"

    oid_cleanerType = "1.3.6.1.2.1.43.11.1.1.6.1.11"
    oid_cleanerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.11"
    oid_cleanerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.11"

    oid_transferType = "1.3.6.1.2.1.43.11.1.1.6.1.12"
    oid_transferCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.12"
    oid_transferRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.12"

    oid_blackTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.1"
    oid_blackTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.1"
    oid_blackTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.1"

    oid_cyanTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.2"
    oid_cyanTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.2"
    oid_cyanTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.2"

    oid_magentaTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.3"
    oid_magentaTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.3"
    oid_magentaTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.3"

    oid_yellowTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.4"
    oid_yellowTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.4"
    oid_yellowTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.4"

    oid_blackDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.5"
    oid_blackDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.5"
    oid_blackDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.5"

    oid_cyanDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.6"
    oid_cyanDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.6"
    oid_cyanDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.6"

    oid_magentaDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.7"
    oid_magentaDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.7"
    oid_magentaDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.7"

    oid_yellowDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.8"
    oid_yellowDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.8"
    oid_yellowDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.8"

    def __init__(
        self,
        ip,
        variant: str,
        description: str,
        port: int = A.CT.PORT.SNMP,
        community: str = "public",
    ):
        super().__init__(-401, ip, port, community)
        self.description = description
        self.variant = type(self).__name__
        self.variant = variant.lower()
        self.accessable: bool | None = None

    def initialize_values(self):
        self.name = self.get_snmp(self.oid_printerName)
        self.model = self.get_snmp(self.oid_printerModel)
        self.serial = self.get_snmp(self.oid_printerSerial)
        self.meta = self.get_snmp(self.oid_printerMeta)

        self.printsOverall = self.get_snmp(self.oid_printsOverall)
        self.printsColor = self.get_snmp(self.oid_printsColor)
        self.printsMonochrome = self.get_snmp(self.oid_printsMonochrome)

        self.fuserType = self.get_snmp(self.oid_fuserType)
        self.fuserCapacity = self.get_snmp(self.oid_fuserCapacity)
        self.fuserRemaining = self.get_snmp(self.oid_fuserRemaining)

        self.wasteType = self.get_snmp(self.oid_wasteType)
        self.wasteCapacity = self.get_snmp(self.oid_wasteCapacity)
        self.wasteRemaining = self.get_snmp(self.oid_wasteRemaining)

        self.cleanerType = self.get_snmp(self.oid_cleanerType)
        self.cleanerCapacity = self.get_snmp(self.oid_cleanerCapacity)
        self.cleanerRemaining = self.get_snmp(self.oid_cleanerRemaining)

        self.transferType = self.get_snmp(self.oid_transferType)
        self.transferCapacity = self.get_snmp(self.oid_transferCapacity)
        self.transferRemaining = self.get_snmp(self.oid_transferRemaining)

        self.blackTonerType = self.get_snmp(self.oid_blackTonerType)
        self.blackTonerCapacity = self.get_snmp(self.oid_blackTonerCapacity)
        self.blackTonerRemaining = self.get_snmp(self.oid_blackTonerRemaining)

        self.cyanTonerType = self.get_snmp(self.oid_cyanTonerType)
        self.cyanTonerCapacity = self.get_snmp(self.oid_cyanTonerCapacity)
        self.cyanTonerRemaining = self.get_snmp(self.oid_cyanTonerRemaining)

        self.magentaTonerType = self.get_snmp(self.oid_magentaTonerType)
        self.magentaTonerCapacity = self.get_snmp(self.oid_magentaTonerCapacity)
        self.magentaTonerRemaining = self.get_snmp(self.oid_magentaTonerRemaining)

        self.yellowTonerType = self.get_snmp(self.oid_yellowTonerType)
        self.yellowTonerCapacity = self.get_snmp(self.oid_yellowTonerCapacity)
        self.yellowTonerRemaining = self.get_snmp(self.oid_yellowTonerRemaining)

        self.blackDrumType = self.get_snmp(self.oid_blackDrumType)
        self.blackDrumCapacity = self.get_snmp(self.oid_blackDrumCapacity)
        self.blackDrumRemaining = self.get_snmp(self.oid_blackDrumRemaining)

        self.cyanDrumType = self.get_snmp(self.oid_cyanDrumType)
        self.cyanDrumCapacity = self.get_snmp(self.oid_cyanDrumCapacity)
        self.cyanDrumRemaining = self.get_snmp(self.oid_cyanDrumRemaining)

        self.magentaDrumType = self.get_snmp(self.oid_magentaDrumType)
        self.magentaDrumCapacity = self.get_snmp(self.oid_magentaDrumCapacity)
        self.magentaDrumRemaining = self.get_snmp(self.oid_magentaDrumRemaining)

        self.yellowDrumType = self.get_snmp(self.oid_yellowDrumType)
        self.yellowDrumCapacity = self.get_snmp(self.oid_yellowDrumCapacity)
        self.yellowDrumRemaining = self.get_snmp(self.oid_yellowDrumRemaining)

        self.accessable = self.ping()

        """
		self.cyanToner = self.get_toner("c")
		self.magentaToner = self.get_toner("m")
		self.yellowToner = self.get_toner("y")
		self.blackToner = self.get_toner("k")

		self.cyanDrum = self.get_drum("c")
		self.magentaDrum = self.get_drum("m")
		self.yellowDrum = self.get_drum("y")
		self.blackDrum = self.get_drum("k")

		self.fuser = self.get_misc("fuser")
		self.cleaner = self.get_misc("cleaner")
		self.waste = self.get_misc("waste")
		self.transfer = self.get_misc("transfer")
		"""

    def get_misc(self, what):
        what = what.lower()
        if what == "fuser":
            remaining = self.fuserRemaining
            capacity = self.fuserCapacity
        if what == "cleaner":
            remaining = self.cleanerRemaining
            capacity = self.cleanerCapacity
        if what == "waste":
            remaining = self.wasteRemaining
            capacity = self.wasteCapacity
        if what == "transfer":
            remaining = self.transferRemaining
            capacity = self.transferCapacity
        try:
            if remaining == -1 or capacity == -1:
                return -1
            if remaining == -404 or capacity == -404:
                return -404
            if remaining == -401 or capacity == -401:
                return -401
            return int(round((int(remaining) / int(capacity)) * 100))
        except:
            return -1

    def ping(self):
        return self.get_snmp(self.oid_printerName) != -404

    @staticmethod
    def isNegative(intTest):
        try:
            int(intTest)
            return True
        except ValueError:
            return False


class Xerox(Printer):
    pass


class XeroxBW(Printer):
    oid_blackDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.6"
    oid_blackDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.6"
    oid_blackDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.6"
    oid_cyanDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.5"
    oid_cyanDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.5"
    oid_cyanDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.5"


class XeroxWC3225(Printer):
    oid_blackDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.2"
    oid_blackDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.2"
    oid_blackDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.2"
    oid_cyanTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.5"
    oid_cyanTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.5"
    oid_cyanTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.5"
    oid_sideCount = "1.3.6.1.4.1.641.6.4.2.1.1.4.1.1"


class HP(Printer):
    oid_printerName = "1.3.6.1.2.1.43.5.1.1.16.1"

    oid_printsOverall = "1.3.6.1.4.1.11.2.3.9.4.2.1.1.16.1.9.0"
    oid_printsColor = "1.3.6.1.4.1.11.2.3.9.4.2.1.1.16.1.10.0"
    oid_printsMonochrome = "1.3.6.1.4.1.11.2.3.9.4.2.1.1.16.1.11.0"


class HPBW(HP):
    oid_fuserType = "1.3.6.1.2.1.43.11.1.1.6.1.2"
    oid_fuserCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.2"
    oid_fuserRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.2"

    oid_printsColor = "1.3.6.1"
    oid_cyanTonerType = "1.3.6.1"
    oid_cyanTonerCapacity = "1.3.6.1"
    oid_cyanTonerRemaining = "1.3.6.1"

    oid_magentaTonerType = "1.3.6.1"
    oid_magentaTonerCapacity = "1.3.6.1"
    oid_magentaTonerRemaining = "1.3.6.1"

    oid_yellowTonerType = "1.3.6.1"
    oid_yellowTonerCapacity = "1.3.6.1"
    oid_yellowTonerRemaining = "1.3.6.1"

    oid_blackDrumType = "1.3.6.1"
    oid_blackDrumCapacity = "1.3.6.1"
    oid_blackDrumRemaining = "1.3.6.1"

    oid_cyanDrumType = "1.3.6.1"
    oid_cyanDrumCapacity = "1.3.6.1"
    oid_cyanDrumRemaining = "1.3.6.1"

    oid_magentaDrumType = "1.3.6.1"
    oid_magentaDrumCapacity = "1.3.6.1"
    oid_magentaDrumRemaining = "1.3.6.1"

    oid_yellowDrumType = "1.3.6.1"
    oid_yellowDrumCapacity = "1.3.6.1"
    oid_yellowDrumRemaining = "1.3.6.1"

    def initialize_values(self):
        Printer.initialize_values(self)
        self.fuserRemaining = round(
            ((int(self.fuserRemaining) / int(self.fuserCapacity)) * 100)
        )


class HPMFP(HP):
    oid_printsOverall = "1.3.6.1.2.1.43.10.2.1.4.1.1"
    oid_printsMonochrome = "1.3.6.1.2.1.43.10.2.1.4.1.1"


class KCSW(Printer):
    oid_printsOverall = "1.3.6.1.4.1.1347.42.2.1.1.1.6.1.1"
    oid_printsMonochrome = "1.3.6.1.4.1.1347.42.2.1.1.1.6.1.1"

    oid_printsColor = "1.3.6.1"
    oid_cyanTonerType = "1.3.6.1"
    oid_cyanTonerCapacity = "1.3.6.1"
    oid_cyanTonerRemaining = "1.3.6.1"

    oid_magentaTonerType = "1.3.6.1"
    oid_magentaTonerCapacity = "1.3.6.1"
    oid_magentaTonerRemaining = "1.3.6.1"

    oid_yellowTonerType = "1.3.6.1"
    oid_yellowTonerCapacity = "1.3.6.1"
    oid_yellowTonerRemaining = "1.3.6.1"

    oid_blackDrumType = "1.3.6.1"
    oid_blackDrumCapacity = "1.3.6.1"
    oid_blackDrumRemaining = "1.3.6.1"

    oid_cyanDrumType = "1.3.6.1"
    oid_cyanDrumCapacity = "1.3.6.1"
    oid_cyanDrumRemaining = "1.3.6.1"

    oid_magentaDrumType = "1.3.6.1"
    oid_magentaDrumCapacity = "1.3.6.1"
    oid_magentaDrumRemaining = "1.3.6.1"

    oid_yellowDrumType = "1.3.6.1"
    oid_yellowDrumCapacity = "1.3.6.1"
    oid_yellowDrumRemaining = "1.3.6.1"

    oid_cleanerType = "1.3.6.1"
    oid_cleanerCapacity = "1.3.6.1"
    oid_cleanerRemaining = "1.3.6.1"


class Brother(Printer):
    oid_blackTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.4"
    oid_blackTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.1"
    oid_blackTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.1"

    def initialize_values(self):
        Printer.initialize_values(self)


class DICL(Printer):
    oid_printsOverall = "1.3.6.1.2.1.43.10.2.1.4.1.1"
    oid_printsColor = "1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.2.2"
    oid_printsMonochrome = "1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.1.2"

    # colorOverall = copiesColor + printsColor - specific to DICL
    oid_copiesColor = "1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.2.1"
    oid_copiesMonochrome = "1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.1.1"

    # Toner
    oid_blackTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.4"
    oid_blackTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.4"
    oid_blackTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.4"

    oid_cyanTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.1"
    oid_cyanTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.1"
    oid_cyanTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.1"

    oid_magentaTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.2"
    oid_magentaTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.2"
    oid_magentaTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.2"

    oid_yellowTonerType = "1.3.6.1.2.1.43.11.1.1.6.1.3"
    oid_yellowTonerCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.3"
    oid_yellowTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.3"

    # Bildtrommel
    oid_blackDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.11"
    oid_blackDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.11"
    oid_blackDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.11"

    oid_cyanDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.5"
    oid_cyanDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.5"
    oid_cyanDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.5"

    oid_magentaDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.7"
    oid_magentaDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.7"
    oid_magentaDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.7"

    oid_yellowDrumType = "1.3.6.1.2.1.43.11.1.1.6.1.9"
    oid_yellowDrumCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.9"
    oid_yellowDrumRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.9"

    # Bildtransferkit
    oid_fuserType = "1.3.6.1.2.1.43.11.1.1.6.1.14"
    oid_fuserCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.14"
    oid_fuserRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.14"

    # Vorlageneinzugskit
    oid_transferType = "1.3.6.1.2.1.43.11.1.1.6.1.15"
    oid_transferCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.15"
    oid_transferRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.15"

    # Resttonbehälter
    oid_wasteType = "1.3.6.1"
    oid_wasteCapacity = "1.3.6.1"
    oid_wasteRemaining = "1.3.6.1"

    # Walzenkit
    oid_cleanerType = "1.3.6.1"
    oid_cleanerCapacity = "1.3.6.1"
    oid_cleanerRemaining = "1.3.6.1"

    def initialize_values(self):
        Printer.initialize_values(self)
        self.printsColor = int(self.printsColor) + int(
            self.get_snmp(self.oid_copiesColor)
        )
        self.printsMonochrome = int(self.printsMonochrome) + int(
            self.get_snmp(self.oid_copiesMonochrome)
        )


class HPM725BW(HPBW):
    oid_cleanerType = "1.3.6.1"
    oid_cleanerCapacity = "1.3.6.1"
    oid_cleanerRemaining = "1.3.6.1"


class OKI(Printer):
    oid_printsOverall = "1.3.6.1"
    oid_printsColor = "1.3.6.1.4.1.2001.1.1.1.1.11.1.10.170.1.6.1"
    oid_printsMonochrome = "1.3.6.1.4.1.2001.1.1.1.1.11.1.10.170.1.7.1"

    oid_fuserType = "1.3.6.1.2.1.43.11.1.1.6.1.10"
    oid_fuserCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.10"
    oid_fuserRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.10"

    oid_transferType = "1.3.6.1.2.1.43.11.1.1.6.1.9"
    oid_transferCapacity = "1.3.6.1.2.1.43.11.1.1.8.1.9"
    oid_transferRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.9"

    oid_wasteType = "1.3.6.1"
    oid_wasteCapacity = "1.3.6.1"
    oid_wasteRemaining = "1.3.6.1"

    oid_cleanerType = "1.3.6.1"
    oid_cleanerCapacity = "1.3.6.1"
    oid_cleanerRemaining = "1.3.6.1"


class PrinterApi:
    VERSION: str = "0.1"

    @staticmethod
    def create_printer(printer_information: PrinterInformation) -> Printer:
        ip: str = printer_information.portName
        variant: str = printer_information.variant.lower()
        description: str = printer_information.description
        if variant == "xerox":
            return Xerox(ip, variant, description)
        elif variant == "xeroxbw":
            return XeroxBW(ip, variant, description)
        elif variant == "hp":
            return HP(ip, variant, description)
        elif variant == "hpbw":
            return HPBW(ip, variant, description)
        elif variant == "hpmfp":
            return HPMFP(ip, variant, description)
        elif variant == "kcsw":
            return KCSW(ip, variant, description)
        elif variant == "dicl":
            return DICL(ip, variant, description)
        elif variant == "hpm725bw":
            return HPM725BW(ip, variant, description)
        elif variant == "xeroxwc3225":
            return XeroxWC3225(ip, variant, description)
        elif variant == "brother":
            return Brother(ip, variant, description)
        return Printer(ip, variant, description)

    @staticmethod
    def create_printer_information(
        value: PrinterADInformation,
    ) -> PrinterInformation:
        variant: str = "xeroxwc3225"
        driverName: str = value.driverName.lower()
        if driverName.find("brother") != -1:
            variant = "brother"
        elif driverName.find("epson") != -1:
            variant = "xerox"
        elif driverName.find("hp") != -1:
            variant = "hpmfp"
        elif driverName.find("kyocera") != -1:
            variant = "kcsw"
        return PrinterInformation(
            value.driverName,
            value.adminDescription,
            value.description,
            value.portName,
            value.serverName,
            value.name,
            variant,
        )

    @staticmethod
    def get_printer_report_for_command(
        printer_ad_information: PrinterADInformation, command: PrinterCommands
    ) -> Printer:
        printer: Printer = PrinterApi.create_printer(
            PrinterApi.create_printer_information(printer_ad_information)
        )
        if command == PrinterCommands.REPORT:
            printer.initialize_values()
            return printer
        elif command == PrinterCommands.STATUS:
            printer.accessable = printer.ping()
            return printer

    @staticmethod
    def call_snmp(printer_ad_information: PrinterADInformation, value: str):
        return PrinterApi.create_printer(
            PrinterApi.create_printer_information(printer_ad_information)
        ).get_snmp(value)
