import logging
import os.path
from typing import Union

from remotemanager.connection.cmd import CMD
from remotemanager.connection.computers.base import BaseComputer
from remotemanager.storage.trackedfile import TrackedFile

logger = logging.getLogger(__name__)


class Script(BaseComputer):
    """
    Subclass of BaseComputer providing the ability to directly execute the scripts
    """

    def __init__(
        self,
        template: str,
        local_dir: str = ".",
        remote_dir: str = ".",
        filename: Union[None, str] = None,
        **kwargs,
    ):
        super().__init__(template, **kwargs)
        filename = filename or f"{abs(self.uuid)}.sh"

        self._file = TrackedFile(local_dir, remote_dir, filename)
        self._cmd = None

    def __hash__(self) -> int:
        return self.uuid

    @property
    def uuid(self) -> int:
        """Returns the hash of the template"""
        return hash(self.template)

    @property
    def exec_cmd(self) -> CMD:
        """Returns the CMD instance that was used to execute the script"""
        return self._cmd

    @property
    def local_dir(self) -> str:
        """Returns the local dir"""
        return self._file.local_dir

    @local_dir.setter
    def local_dir(self, path: str):
        """Sets the local dir, if possible"""
        if self.exec_cmd is not None:
            raise ValueError("Cannot set path on an executed run, set at run()")
        self._file._local_path = path

    @property
    def remote_dir(self) -> str:
        """Returns the remote dir"""
        return self._file.remote_dir

    @remote_dir.setter
    def remote_dir(self, path: str):
        """Sets the remote dir, if possible"""
        if self.exec_cmd is not None:
            raise ValueError("Cannot set path on an executed run, set at run()")
        self._file._remote_path = path

    @property
    def local_path(self) -> str:
        """Full local path"""
        return self._file.local

    @property
    def remote_path(self) -> str:
        """Full remote path"""
        return self._file.remote

    @property
    def filename(self) -> str:
        """Returns the filename"""
        return self._file.name

    @property
    def file(self) -> TrackedFile:
        """Returns the TrackedFile instance for this script"""
        return self._file

    def run(
        self,
        exectuable: str = "bash",
        local_dir: Union[None, str] = None,
        remote_dir: Union[None, str] = None,
        stream: bool = False,
        cleanup: bool = True,
        **kwargs,
    ) -> str:
        """
        Attempt to run the current script on the remote

        Args:
            exectuable (str): exectuable to call
            local_dir (str): update local_dir
            remote_dir (str): update remote_dir
            stream (bool): stream output
            cleanup (bool): Delete files after execution if True
            kwargs (dict): args to pass to script() method
        """
        self._cmd = None
        if local_dir is not None:
            self.local_dir = local_dir
        if remote_dir is not None:
            self.remote_dir = remote_dir

        script = self.script(**kwargs)

        self.file.write(script)

        if self.local_path != self.remote_path:
            self.transport.queue_for_push(self.file)
            self.transport.transfer()
        else:
            logger.debug("local and remote paths are equal, ignoring transfer")

        cmd = [f"cd {self.file.remote_dir} && {exectuable} {self.file.name}"]

        if cleanup:
            cmd.append(f" && rm {self.file.remote}")

        self._cmd = self.cmd(
            "".join(cmd),
            stream=stream,
            raise_errors=False,
        )
        self._cmd.exec()

        if cleanup:
            try:
                os.remove(self.file.local)
            except FileNotFoundError:
                pass

        return self.exec_cmd.stdout

    @property
    def stdout(self) -> Union[None, str]:
        """Returns the stdout of the run, if available"""
        if self.exec_cmd is not None:
            return self.exec_cmd.stdout
        return None

    @property
    def stderr(self) -> Union[None, str]:
        """Returns the stderr of the run, if available"""
        if self.exec_cmd is not None:
            return self.exec_cmd.stderr
        return None
