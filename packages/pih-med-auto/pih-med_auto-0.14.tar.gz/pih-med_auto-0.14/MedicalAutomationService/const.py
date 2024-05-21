import ipih

from pih import A
from pih.collections.service import ServiceDescription

NAME: str = "MedicalAutomation"

HOST = A.CT_H.BACKUP_WORKER

VERSION: str = "0.14"

PACKAGES: tuple[str, ...] = (
    A.PTH_FCD_DIST.NAME(A.CT_SR.MOBILE_HELPER.standalone_name),  # type: ignore
)

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Medical Automation service",
    host=HOST.NAME,
    version=VERSION,
    standalone_name="med_auto",
    use_standalone=True,
    packages=PACKAGES,
)


VALENTA_SOURCE_HOST: str = A.CT_H.WS816.NAME