import os
import shutil
from fabric.operations import local

COVERAGE_REPORT_HTML_DIR = 'coverage_html'
COVERAGE_REPORT_FILE = '.coverage'


def cq() -> None:
    """Run Code quality chcker."""
    local('flake8 --config=flake8.ini')


def test() -> None:
    """Run all tests."""
    local('python manage.py test')


def coverage() -> None:
    """Runs tests with coverage report."""
    if os.path.exists(COVERAGE_REPORT_HTML_DIR):
        shutil.rmtree(COVERAGE_REPORT_HTML_DIR)

    if os.path.isfile(COVERAGE_REPORT_FILE):
        os.remove(COVERAGE_REPORT_FILE)

    local("coverage run --source='.' manage.py test")

    local("coverage report --skip-covered")
    local("coverage html")
