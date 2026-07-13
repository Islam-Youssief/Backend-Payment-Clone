import time
import logging
import subprocess
import sys

import bolt.api as btapi


class OneDirTestTask:
    def __init__(self):
        self.process = None

    def __call__(self, **kwargs):
        self._configure()
        self._execute()

    def _configure(self):
        self.test_file = input("Enter the test file path: ")
        if not self.test_file: raise NoTestFileSpecifiedError()

    def _execute(self):
        args = [sys.executable, "-m", "pytest", "-s", self.test_file]
        logging.error('Subprocess arguments: ' + str(args))
        self.process = self._popen_script(args)

    def _popen_script(self, args):
        return subprocess.Popen(args)



class NoTestFileSpecifiedError(btapi.RequiredConfigurationError):
    def __init__(self):
        super().__init__("test file")
