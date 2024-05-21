import ipih

from pih import A
from pih.collections.service import ServiceDescription


NAME: str = "RegistratorAutomation"

HOST = A.CT_H.BACKUP_WORKER


PACKAGES: tuple[str, ...] = (
    A.PTH_FCD_DIST.NAME(A.CT_SR.MOBILE_HELPER.standalone_name),  # type: ignore
)

VERSION: str = "0.14"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Registrator Automation service",
    host=HOST.NAME,
    version=VERSION,
    standalone_name="rgst_auto",
    use_standalone=True,
    packages=PACKAGES,
)
