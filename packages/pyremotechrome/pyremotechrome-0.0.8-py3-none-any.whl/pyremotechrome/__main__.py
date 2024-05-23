"""
Use this module to start the server
"""

from typing import Generator, Any
from os.path import dirname, realpath
from subprocess import Popen, PIPE
from pyremotechrome.config import Conf


c = Conf()
__ROOT__ = f"{dirname(realpath(__file__))}"
__PYTHON_EXEC__ = c.server.python_executable_path


def readline_from_server() -> Generator[list[str], Any, None]:
    """Start the server"""
    proc_args = [__PYTHON_EXEC__, f"{__ROOT__}/server/server.py"]
    proc = Popen(proc_args, stdout=PIPE, universal_newlines=True)
    for stdout in iter(proc.stdout.readlines, ""):
        yield stdout

    proc.stdout.close()
    code = proc.wait()
    if code:
        raise Exception("Server exited unexceptedly.")

if __name__ == "__main__":
    for line in readline_from_server():
        print(line, end="")
