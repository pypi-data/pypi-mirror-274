import importlib.util
import sys

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from SSHService.api import SSHApi
from pih import A

name: str = "svshost.fmv.lan"
for item in SSHApi.LOGIN_PASSWORD_PAIRS_MAP:
    if A.D.contains(item, name):
        print(0)
