import os
import sys

import bolt

import api.core.configurations as conf
# Development tasks
bolt.register_task('ut', ['clear-pyc', 'shell.pytest'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('cov', ['clear-pyc', 'shell.pytest.coverage'])
# Helper tasks
bolt.register_task('clear-pyc', [
    'delete-pyc',
    'delete-pyc.from-tests'
])
bolt.register_task('start-wiremock', [
    'shell.start-wiremock'
])

bolt.register_task('generate-docs', [
    'shell.generate-rst-docs',
    'shell.generate-html-docs'
])

# Directories
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, 'svc')
TEST_DIR = os.path.join(PROJECT_ROOT, 'tests')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
TOOLS_DIR = os.path.join(PROJECT_ROOT, 'tools')
TEST_COVERAGE_DIR = os.path.join(OUTPUT_DIR, 'coverage')
GENERATED_DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs', 'generated')
# Files
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, 'requirements-dev.txt')

# Wiremock vars
WIREMOCK_PATH = os.path.join(TOOLS_DIR, 'wiremock')
WIREMOCK_JAR_PATH = os.path.join(WIREMOCK_PATH, 'wiremock-standalone-2.31.0.jar')

config = {
    'pip': {
        'command': 'install',
        'options': {
            'r': REQUIREMENTS_FILE,
        }
    },
    'delete-pyc': {
        'sourcedir': SRC_DIR,
        'recursive': True,
        'from-tests': {
            'sourcedir': TEST_DIR,
        }
    },
    "shell": {
        "pytest": {
            "command": sys.executable,
            "arguments": ["-m", "pytest", TEST_DIR],
            "coverage": {
                "arguments": [
                    "-m",
                    "pytest",
                    f"--cov=svc",
                    "--cov-report",
                    f"html:{TEST_COVERAGE_DIR}",
                    TEST_DIR,
                ]
            },
        },
        'start-wiremock': {
            'command': 'java',
            'arguments': [
                '-jar',
                WIREMOCK_JAR_PATH,
                '--root', WIREMOCK_PATH,
                '--global-response-templating', 'true',
                '--port', conf.AppConfig().wiremock_port
            ]
        },

        'generate-rst-docs': {
            'command': 'sphinx-apidoc',
            'arguments': ['-o', GENERATED_DOCS_DIR, 'module1']
        },
        'generate-html-docs': {
            'command': 'sphinx-build',
            'arguments': ['-b', 'html', 'docs', 'docs/_build']
        }
    },
    'conttest': {
        'task': 'ut',
        'directory': PROJECT_ROOT
    },
    'mkdir': {
        'unit': {
            'directory': TEST_COVERAGE_DIR
        }
    },
}
