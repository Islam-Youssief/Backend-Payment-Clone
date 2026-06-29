import os
import sys

import bolt

import api.core.configurations as conf
# Development tasks
bolt.register_task('ut', ['clear-pyc', 'shell.pytest'])
bolt.register_task('ct', ['conttest'])
<<<<<<< HEAD
=======
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
bolt.register_task('start-wiremock', ['shell.start-wiremock'])
>>>>>>> 033556c (feat: implement Fawry payment integration schema and Wiremock)
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
<<<<<<< HEAD
SRC_DIR = os.path.join(PROJECT_ROOT, 'svc')
TEST_DIR = os.path.join(PROJECT_ROOT, 'tests')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
TOOLS_DIR = os.path.join(PROJECT_ROOT, 'tools')
TEST_COVERAGE_DIR = os.path.join(OUTPUT_DIR, 'coverage')
GENERATED_DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs', 'generated')
=======
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
WIREMOCK_PATH = os.path.join(PROJECT_ROOT, 'tools', 'wiremock')
WIREMOCK_JAR_PATH = os.path.join(WIREMOCK_PATH, 'wiremock-standalone-2.31.0.jar')
WIREMOCK_PORT = '8000'
>>>>>>> 033556c (feat: implement Fawry payment integration schema and Wiremock)
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
<<<<<<< HEAD
            'arguments': ['-b', 'html', 'docs', 'docs/_build']
=======
            'arguments': ['-b', 'html', DOCS_DIR, CODE_DOCUMENTATION_DEST_DIR]
        },
        "npm-run": {
            "command": 'npm',
            "arguments": ['run', 'dev']
        },
        "start-wiremock": {
            "command": "java",
            "arguments": [
                "-jar", WIREMOCK_JAR_PATH,
                "--port", WIREMOCK_PORT,
                "--root-dir", WIREMOCK_PATH
            ]
>>>>>>> 033556c (feat: implement Fawry payment integration schema and Wiremock)
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
<<<<<<< HEAD
=======
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
>>>>>>> 033556c (feat: implement Fawry payment integration schema and Wiremock)
}
