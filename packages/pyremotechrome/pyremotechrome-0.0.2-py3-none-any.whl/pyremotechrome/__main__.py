"""
Use this module to start the server
"""

from sys import argv
from os.path import dirname, realpath
from subprocess import Popen, PIPE, STDOUT
from pyremotechrome.config import MegaConf


c = MegaConf()
__ROOT__ = f"{dirname(realpath(__file__))}"
__PYTHON_EXEC__ = c.server.python_executable_path


def start() -> None:
    """Start the server"""
    proc_args = [__PYTHON_EXEC__, f"{__ROOT__}/server/server.py"]
    proc = Popen(proc_args, stdout=PIPE, stderr=STDOUT)
    proc.wait()


if __name__ == "__main__":
    if len(argv) > 1:
        print("Invalid argument(s).")
        exit(0)

    start()
