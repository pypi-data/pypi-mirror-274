import ipih

from pih import A
from SSHService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD, as_standalone=as_standalone):
        
        from SSHService.api import SSHApi as Api
        from pih.tools import ParameterList, js, j, escs
        
        from typing import Any

        api: Api = Api()

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:
            if sc == SC.mount_facade_for_linux_host:
                host: str = pl.next()
                api.execute_command(
                    js(("mkdir", A.PTH.FACADE.LINUX_MOUNT_POINT_PATH)), host, use_sudo=True
                )
                api.execute_command(
                    js(
                        (
                            "mount -t cifs",
                            escs(A.PTH.for_windows(A.PTH.FACADE.STORAGE())),
                            A.PTH.FACADE.LINUX_MOUNT_POINT_PATH,
                            j(
                                (
                                    "-o username=",
                                    A.D_V.value(A.CT_LNK.ADMINISTRATOR_LOGIN, True),
                                    ",",
                                    "password=",
                                    A.D_V.value(A.CT_LNK.ADMINISTRATOR_PASSWORD, True),
                                )
                            ),
                        )
                    ),
                    host,
                    use_sudo=True,
                )
                return True
            if sc == SC.execute_ssh_command:
                return A.R.pack(
                    A.CT_FC.VALUE_LIST,
                    api.execute_command(
                        pl.next(), pl.next(), pl.next(), pl.next(), pl.next(), pl.next()
                    ),
                )
            if sc == SC.get_certificate_information:
                return A.R.pack(
                    A.CT_FC.VALUE,
                    api.get_certificate_information(pl.next(), pl.next(), pl.next()),
                )
            if sc == SC.get_unix_free_space_information_by_drive_name:
                return A.R.pack(
                    A.CT_FC.VALUE,
                    api.get_unix_free_space_information_by_drive_name(
                        pl.next(), pl.next(), pl.next()
                    ),
                )
            return None

        A.SRV_A.serve(SD, service_call_handler, isolate=ISOLATED, as_standalone=as_standalone)
        
if __name__ == "__main__":
    start()
