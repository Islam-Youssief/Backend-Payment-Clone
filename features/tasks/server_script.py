"""
This module provides tasks to manage external services that need to be instantiated for other tasks to use.
"""
import logging
import subprocess
import sys

import bolt.api as btapi


STARTUP_SCRIPT = 'run-script'


class StartServerServiceTask:
    """
    This task allows to start a server through a startup script. 
    The application will be available until the execution script is completed. 
    The following shows how this task can be configured:

    ..  code-block:: python

        import bolt
        import features.tasks.flask as flask_tasks

        bolt.register_module_tasks(flask_tasks)

        config = {
            'startup-server': {
                'run-script': 'the/startup/script.py'
            }
        }
    """

    def __init__(self):
        self.process = None

    def __call__(self, **kwargs):
        self.config = kwargs.get('config')
        self._configure()
        self._execute()

    def tear_down(self):
        if self.process:
            self._terminate(self.process)

    def _configure(self):
        self.startup_script = self.config.get(STARTUP_SCRIPT)
        if not self.startup_script: raise StartupScriptNotSpecifiedError()

    def _execute(self):
        logging.info(f'Starting app through script: {self.startup_script}')
        args = [sys.executable, self.startup_script]
        logging.debug('Subprocess arguments: ' + str(args))
        self.process = self._popen_script(args)

    def _popen_script(self, args):
        return subprocess.Popen(args)

    def _terminate(self, process):
        process.terminate()


class StartupScriptNotSpecifiedError(btapi.RequiredConfigurationError):
    def __init__(self):
        super().__init__(STARTUP_SCRIPT)
