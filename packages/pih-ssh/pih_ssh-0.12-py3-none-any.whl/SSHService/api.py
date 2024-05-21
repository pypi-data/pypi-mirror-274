import ipih

from pih import A
from pih.tools import e, j, js, ne, jnl
from SSHService.const import LOGIN_PASSWORD_PAIRS_MAP

from paramiko import AutoAddPolicy, SSHClient


class SSHApi:
    def get_login_password_pair(self, host: str) -> tuple[str, str] | None:
        login_password_pair: tuple[str, str] | None = None
        for login_passwor_pair_item in LOGIN_PASSWORD_PAIRS_MAP:
            login_passwor_pair_item_host: str = A.D.get(login_passwor_pair_item)
            if (
                login_passwor_pair_item_host == host
                or login_passwor_pair_item_host == A.D_F.host_name(host)
            ):
                login_password_pair = LOGIN_PASSWORD_PAIRS_MAP[login_passwor_pair_item]
                break
        return login_password_pair

    def execute_command(
        self,
        command: str,
        host: str,
        username: str | None = None,
        password: str | None = None,
        use_sudo: bool = False,
        in_background: bool = False,
    ) -> list[str]:
        login_password_pair: tuple[str, str] | None = self.get_login_password_pair(host)
        username = username or login_password_pair[0]
        password = password or login_password_pair[1]
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(host, username=username, password=password, look_for_keys=False)
        if use_sudo:
            command = A.SYS.make_sudo(command, password)
        if in_background:
            command = js(
                ("nohup", command, ">/dev/null", "2>&1", "</dev/null & echo $!")
            )
        _, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        result: list[str] = ssh_stdout.readlines()
        error: list[str] = ssh_stderr.readlines()
        ssh.close()
        if e(result) and ne(error):
            return A.ER.rpc(message=jnl((error)))
        return result

    def get_unix_free_space_information_by_drive_name(
        self,
        drive_name: str,
        host: str,
        username: str | None = None,
        password: str | None = None,
    ) -> str | None:
        login_password_pair: tuple[str, str] | None = self.get_login_password_pair(host)
        username = username or login_password_pair[0]
        password = password or login_password_pair[1]
        result: list[str] = self.execute_command("df -h", host, username, password)
        for item in result:
            index: int = item.find(drive_name)
            if index != -1:
                result: list[str] = js(
                    A.D.filter(
                        lambda item: ne(item),
                        item[index + len(drive_name) :].strip().split(" "),
                    )[2:]
                ).split(" ")[:2]
                result[1] = j((100 - int(result[1][0:-1]), result[1][-1]))
                return js(result)
        return None

    def get_certificate_information(
        self, host: str, username: str | None = None, password: str | None = None
    ) -> str | None:
        login_password_pair: tuple[str, str] | None = self.get_login_password_pair(host)
        username = username or login_password_pair[0]
        password = password or login_password_pair[1]
        cut_value: str = "Expiry Date"
        certificate_list: list[str] = self.execute_command(
            "certbot certificates", host, username, password
        )

        def get_item(index: int) -> str:
            return certificate_list[index].strip()

        for index in range(len(certificate_list)):
            value: str = get_item(index)
            if value.find("Certificate Name") != -1 and (
                value.find(f" {host}") + len(host) + 1 == len(value)
            ):
                index += 1
                while True:
                    value = get_item(index)
                    if value.find(cut_value) != -1:
                        return value[len(cut_value) + 2 :]
                    index += 1
        return None
