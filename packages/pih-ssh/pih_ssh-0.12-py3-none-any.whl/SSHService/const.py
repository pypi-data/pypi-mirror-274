import ipih

from pih import A
from pih.consts.ssh_hosts import SSHHosts
from pih.collections.service import ServiceDescription

NAME: str = "SSH"

HOST = A.CT_H.BACKUP_WORKER

VERSION: str ="0.12"

PACKAGES: tuple[str, ...] = ("paramiko",)

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="SSH service",
    host=HOST.NAME,
    commands=(
        "execute_ssh_command",
        "get_certificate_information",
        "get_unix_free_space_information_by_drive_name",
        "mount_facade_for_linux_host"
    ),
    use_standalone=True,
    standalone_name="ssh",
    version=VERSION,
    packages=PACKAGES,
)

LOGIN_PASSWORD_PAIRS_MAP: dict[SSHHosts, tuple[str, str]] = {
    SSHHosts.EMAIL_SERVER: ("root", "nBTeNVEj7J"),
    SSHHosts.SITE_API: ("root", "9GLm_5d6B!VFG"),
    SSHHosts.SITE: ("root", "@yeZqf_WcDxCQ!"),
    SSHHosts.SERVICES: (
        A.D_V_E.value(A.CT_LNK.SERVICES_USER_LOGIN),
        A.D_V_E.value(A.CT_LNK.SERVICES_USER_PASSWORD),
    ),
}
