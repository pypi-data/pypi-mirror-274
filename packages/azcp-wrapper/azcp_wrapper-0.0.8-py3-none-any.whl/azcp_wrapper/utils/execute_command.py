import os
import subprocess

from typing import List, Generator, Union
from pathlib import Path, WindowsPath
from azcp_wrapper.logging_config import logger


def execute_command(cmd: List[str]) -> Generator[Union[WindowsPath, str], None, None]:
    """
    Executes a command while simultaneously sending output.
    """
    logger.info(f"Executing command -> {' '.join(str(ruta) for ruta in cmd)}")
    popen = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=os.environ.copy(),
    )

    if popen.stdout is not None:
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line

        popen.stdout.close()
        return_code = popen.wait()

        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)
