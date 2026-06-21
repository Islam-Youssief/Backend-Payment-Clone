import os
import sys

import bolt
import behave_restful.bolt_behave_restful as bbr


# For registering tasks
bolt.register_module_tasks(bbr)


# Development tasks
bolt.register_task('install', ['shell.uv-sync'])
bolt.register_task('lint', ['shell.ruff-check', 'shell.ruff-format'])
bolt.register_task('ut', ['clear-pyc', 'shell.pytest'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('ft', [
    'clear-pyc',
    'startup-flask',
    'start-wiremock',
    'sleep',
    'behave-restful',
])
bolt.register_task('ft-current', [
    'clear-pyc',
    'startup-flask',
    'start-wiremock',
    'sleep',
    'behave-restful.current',
])
bolt.register_task('ft-wip', [
    'clear-pyc',
    'startup-flask',
    'start-wiremock',
    'sleep',
    'behave-restful.wip',
])
bolt.register_task('start-dev', [
    'clear-pyc',
    'startup-flask',
    'start-wiremock',
    'sleep',
    # 'behave-restful.current',
    'shell.npm-run',
    'sleep.infinitely',
])
bolt.register_task('cov', ['clear-pyc', 'shell.pytest.coverage'])
bolt.register_task('test-report', ['clear-pyc', 'shell.pytest.terminal-cov'])
bolt.register_task('ot', ['clear-pyc', 'one-dir-test'])
# Helper tasks
bolt.register_task('clear-pyc', [
    'delete-pyc',
    'delete-pyc.from-tests'
])
# Generate documentation tasks
bolt.register_task('generate-docs', [
    'shell.generate-rst-docs',
    'shell.generate-html-docs'
])

# Directories
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
API_DIR = os.path.join(PROJECT_ROOT, 'api')
FEATURES_DIR = os.path.join(PROJECT_ROOT, 'features')
TOOLS_DIR = os.path.join(FEATURES_DIR, 'tools')
TEST_DIR = os.path.join(PROJECT_ROOT, 'tests', 'test_api')
BUILD_DIR = os.path.join(PROJECT_ROOT, 'build')
DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')
GENERATED_DOCS_DIR = os.path.join(DOCS_DIR, 'generated')
CODE_DOCUMENTATION_DEST_DIR = os.path.join(BUILD_DIR, 'code-docs')
TEST_COVERAGE_DEST_DIR = os.path.join(BUILD_DIR, 'coverage')

# Wiremock
WIREMOCK_PATH = os.path.join(TOOLS_DIR, 'wiremock')
WIREMOCK_JAR_PATH = os.path.join(WIREMOCK_PATH, 'wiremock-standalone-3.13.1.jar')
WIREMOCK_PORT = '8000'
# Files
START_UP_SCRIPT = os.path.join(PROJECT_ROOT, 'run.py')


config = {
    'delete-pyc': {
        'sourcedir': API_DIR,
        'recursive': True,
        'from-tests': {
            'sourcedir': TEST_DIR,
        }
    },
    "shell": {
        "uv-sync": {
            "command": "uv",
            "arguments": ["sync", "--frozen"],
        },
        "ruff-check": {
            "command": "uvx",
            "arguments": ["ruff", "check", API_DIR],
        },
        "ruff-format": {
            "command": "uvx",
            "arguments": ["ruff", "format", "--check", API_DIR],
        },
        "pytest": {
            "command": sys.executable,
            "arguments": ["-m", "pytest", "-s", TEST_DIR],
            "terminal-cov": {
                "arguments": [
                    "-m",
                    "pytest",
                    f"--cov={API_DIR}",
                    TEST_DIR
                ]
            },
            "coverage": {
                "arguments": [
                    "-m",
                    "pytest",
                    "-s",
                    f"--cov={API_DIR}",
                    "--cov-report",
                    f"html:{TEST_COVERAGE_DEST_DIR}",
                    TEST_DIR,
                ]
            },
        },
        'generate-rst-docs': {
            'command': 'sphinx-apidoc',
            'arguments': ['-o', GENERATED_DOCS_DIR, API_DIR]
        },
        'generate-html-docs': {
            'command': 'sphinx-build',
            'arguments': ['-b', 'html', DOCS_DIR, CODE_DOCUMENTATION_DEST_DIR]
        },
        "npm-run": {
            "command": 'npm',
            "arguments": ['run', 'dev']
        }
    },
    'conttest': {
        'task': 'ut',
        'directory': PROJECT_ROOT
    },
    'mkdir': {
        'unit': {
            'directory': TEST_COVERAGE_DEST_DIR
        }
    },
    'sleep': {
        'duration': 5,
        'infinitely': {
            'duration': -1,
        },
        'ci': {
            'duration': 10
        }
    },
    'startup-flask': {
        'startup-script': START_UP_SCRIPT,
    },
    'start-wiremock': {
        'jar-path': WIREMOCK_JAR_PATH,
        'options': {
            'root_dir': WIREMOCK_PATH,
            'port': WIREMOCK_PORT,
            'global-response-templating': True,
            'enable-browser-proxying': True,
            'enable-stub-cors': True,
        }
    },
    'behave-restful': {
        'directory': FEATURES_DIR,
        'definition': 'local',
        'options': {
            'tags': [
                ['~@disabled'],
                ['~@wip']
            ],
            'format': 'progress2'
        },
        'wip': {
            'options': {
                'tags': ['@wip']
            }
        },
        'current': {
            'options': {
                'tags': [
                    ['@current'],
                    ['~@wip']
                ],
                'format': 'progress2',
                'show-skipped': False,
                'capture': False,
                'capture-stderr': False
            }
        },
    },
}
