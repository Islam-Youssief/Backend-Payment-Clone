"""
This module provides tasks to manage wiremock that need to be instantiated for other tasks to use.
"""

import logging
import os
import subprocess

import requests
import bolt.api as bolt_api


TASK_START_WIREMOCK = 'start-wiremock'


class ArgumentBuilder:
    def __init__(self):
        self._base_args = ["java", "-jar"]

    def build(self, jar_path, options):
        """
        Build the argument list for executing a JAR file.

        :param jar_path: Path to the JAR file.
        :param options: Dictionary of options and their values.
        :return: A list of arguments ready for subprocess execution.
        """

        if not jar_path:
            raise bolt_api.RequiredConfigurationError("jar-path")
        args = [*self._base_args, jar_path]
        for option, value in options.items():
            opt = f"--{option.replace('_', '-')}"
            args.append(opt) if isinstance(value, bool) and value else args.extend([opt, str(value)])
        return args


class StartWiremockTask(bolt_api.Task):
    def __init__(self, os_test=None, builder=None):
        self.os = os_test or os
        self.builder = builder or ArgumentBuilder()

    def tear_down(self):
        if self.process: self._terminate()

    def _configure(self):
        self.jar_path = self.config.get('jar-path')
        self.options = self.config.get('options', {})
        self.url = self.options.get('url', 'http://127.0.0.1')
        self.port = self.options.get('port', '8080')
        logging.info(f'Starting Wiremock using {self.jar_path}')
        self.args = self.builder.build(self.jar_path, self.options)
        logging.info(f'Command line arguments: {self.args}')

    def _execute(self):
        self.process = self._popen()

    def _popen(self):
        s_args = ' '.join(self.args)
        return subprocess.Popen(s_args, shell=True)

    def _terminate(self):
        requests.post(f'{self.url}:{self.port}/__admin/shutdown')


def register_tasks(registry):
    registry.register_task(TASK_START_WIREMOCK, StartWiremockTask())
