"""
The main.py module acts as a cli interface to parse
the user inputs in command line
and executes related function from dependencies.py module.
"""
# Third party library imports
import click

# Local application imports
from .dependencies import *


def common_options(function):
    """
    Decorator to define common click options.
    """
    function = click.option('-v', '--venv_path', 
                            prompt="Enter the path to the virtual environment",
                            help="Path to the virtual environment")(function)
    function = click.option('-l', '--language',
                            prompt="Enter the language",
                            type=click.Choice(['python', 'cpp']),
                            help="Project language to manage the dependencies")(function)
    return function

def requirements_option(function):
    """
    Decorator for the requirements file option.
    """
    return click.option('-r', '--requirements_file',
                        prompt="Enter the requirements.txt file full path",
                        required=True,
                        help="Path to requirements file")(function)


@click.group()
@click.version_option()
def cli():
    """Command Line Interface for managing project dependencies."""
    pass


@cli.command()
@common_options
@requirements_option
def install(venv_path, requirements_file, language):
    """Install dependencies from a requirements file."""
    install_dependencies(requirements_file, language, venv_path)

@cli.command()
@common_options
@click.option('-p', '--package_name',
              prompt="Enter the package name you need to uninstall",
              required=True,
              help="Package name to uninstall")
def uninstall(venv_path, language, package_name):
    """Uninstall a package."""
    uninstall_dependency(package_name, language, venv_path)

@cli.command()
@common_options
def list(venv_path, language):
    """List installed packages."""
    list_dependencies(language, venv_path)

@cli.command()
@common_options
@requirements_option
def update(venv_path, requirements_file, language):
    """Update dependencies from a requirements file."""
    update_dependencies(requirements_file, language, venv_path)

@cli.command()
@common_options
@click.option('-lf', '--lock_file',
              prompt="Enter the lock file name with its absolute path",
              required=True,
              help="Name of the lock file to lock and save dependencies")
def lock(venv_path, language, lock_file):
    """Generate a lock file for dependencies."""
    lock_dependencies(lock_file, language, venv_path)

@cli.command()
@click.option('-v', '--venv_path', 
              prompt="Enter the path to the virtual environment",
              help="Path to the virtual environment")
@click.option('-sc', '--source_code_full_path', 
              prompt="Enter the path to the source code directory in virtual environment",
              help="Path to the source code directory")
def remove_unused(venv_path, source_code_full_path):
    """Remove unused dependencies.
    - Currently this feature is supported for python projects only.
    """
    remove_unused_dependencies(venv_path, source_code_full_path)

@cli.command()
@click.option('-r', '--requirements_file',
              prompt="Enter the relative path to the requirements.txt file",
              required=True,
              help="Path to requirements file")
@click.option('-td', '--tests_dir', required=True,
              prompt="Enter the relative path to the tests directory of the project",
              help="Name of the directory containing the project's tests")
def containerize_and_test(requirements_file, tests_dir):
    """
    Containerize and run the tests.

    Before running, ensure the following requirements are met:
    - Only applicable to Python projects.
    - Execute within an active virtual environment.
    - 'deps-manager' must be installed in the virtual environment.
    - Docker must be installed and running.
    """
    containerize_and_run_tests(requirements_file, tests_dir)


if __name__ == '__main__':
    cli()
