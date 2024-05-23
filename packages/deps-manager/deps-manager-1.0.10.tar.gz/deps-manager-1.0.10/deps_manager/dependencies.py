"""
This module handles all dependency management operations based on the language.
"""

# Python standard library imports
import subprocess
import os

# Local application imports
from .utils import handle_error


def print_divider(spacing=0):
    """
    Print a divider with the specified character and length.
    """
    # Create the divider
    divider = "#" * 67

    # Print with specified spacing
    print("\n" * spacing + divider)

@handle_error
def install_dependencies(requirements_file, language, venv_path):
    """
    Installs dependencies.
    """
    if language == 'python':
        pip_executable = 'pip'
        if venv_path:
            pip_executable = f"{venv_path}/bin/pip"  # For Linux and MacOS
        subprocess.run([pip_executable, 'install', '-r',
                        requirements_file], check=True)
    
    elif language == 'cpp':
        subprocess.run(['conan', 'install', '-r', requirements_file],
                        check=True)

@handle_error
def uninstall_dependency(package, language, venv_path):
    """
    Uninstalls dependencies.
    """
    if language == 'python':
        pip_executable = 'pip'
        if venv_path:
            pip_executable = f"{venv_path}/bin/pip"  # For Linux and MacOS
        subprocess.run([pip_executable, 'uninstall', '-y', package], check=True)
    elif language == 'cpp':
        subprocess.run(['conan', 'uninstall', '-y', package], check=True)

@handle_error
def list_dependencies(language, venv_path):
    """
    Lists dependencies.
    """
    if language == 'python':
        pip_executable = 'pip'
        if venv_path:
            pip_executable = f"{venv_path}/bin/pip"  # For Linux and MacOS
        subprocess.run([pip_executable, 'list'], check=True)
    elif language == 'cpp':
        subprocess.run(['conan', 'list'], check=True)

@handle_error
def update_dependencies(requirements_file, language, venv_path):
    """
    Updates dependencies.
    """
    if language == 'python':
        pip_executable = 'pip'
        if venv_path:
            pip_executable = f"{venv_path}/bin/pip"  # For Linux and MacOS
        subprocess.run([pip_executable, 'install', '--upgrade', '-r',
                        requirements_file], check=True)
    elif language == 'cpp':
        subprocess.run(['conan', 'install', '--update', requirements_file], check=True)

@handle_error
def lock_dependencies(requirements_lock_file, language, venv_path):
    """
    Build a lockfile to lock current dependencies.
    """
    if language == 'python':
        pip_executable = 'pip'
        if venv_path:
            pip_executable = f"{venv_path}/bin/pip" # For Linux and MacOS
        subprocess.run([pip_executable, 'freeze'],
                        stdout=open(requirements_lock_file, "w"), check=True)
    elif language == 'cpp':
        subprocess.run(['conan', 'lock', requirements_lock_file], check=True)

@handle_error
def ensure_pipreqs_installed(pip_executable):
    """
    Ensure pipreqs is installed in the virtual environment.
    """
    # Check if pipreqs is installed
    try:
        subprocess.run([pip_executable, 'show', 'pipreqs'], 
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # If not installed, install it
        print("pipreqs is not installed. Installing now...")
        subprocess.run([pip_executable, 'install', 'pipreqs'], check=True)

@handle_error
def remove_unused_dependencies(venv_path, source_code_full_path):
    """
    Remove unused dependencies.
    """
    pip_executable = 'pip'
    if venv_path:
        pip_executable = f"{venv_path}/bin/pip"
    
    # Get current packages
    current_reqs = subprocess.run([pip_executable, 'freeze'],
                                    capture_output=True, text=True)
    current_packages = set([line.split('==')[0] for line in current_reqs.stdout.splitlines()])

    # Ensure pipreqs is installed
    ensure_pipreqs_installed(pip_executable)

    # Delete existing requirements.txt if it exists
    requirements_file_path = f"{source_code_full_path}/requirements.txt"

    if os.path.exists(requirements_file_path):
        os.remove(requirements_file_path)

    # Run pipreqs to generate a new requirements.txt
    pipreqs_executable = f"{venv_path}/bin/pipreqs"
    subprocess.run([pipreqs_executable, source_code_full_path, '--encoding', 'utf-8'], check=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read the generated requirements.txt to get used packages
    with open(requirements_file_path, "r") as f:
        used_packages = set(line.split("==")[0] for line in f.readlines())

    # Uninstall unused dependencies
    unused_packages = current_packages - used_packages
    
    for package in unused_packages:
        subprocess.run([pip_executable, 'uninstall', '-y', package], check=True)
    
    print_divider(2)
    print("Packages that were installed:")
    for package in current_packages:
        print(f" - {package}")
    print_divider()
    print_divider(2)
    print("Packages that are needed for the project:")
    for package in used_packages:
        print(f" - {package}")
    print_divider()

    if unused_packages:
        print_divider(2)
        print("The following unused packages have been removed:")
        for package in unused_packages:
            print(f" - {package}")
        print_divider()
    else:
        print_divider(2)
        print("No unused packages to remove.")
        print_divider()

def is_deps_manager_installed():
    """Helper function to check if deps-manager is installed in venv."""
    try:
        subprocess.run(
            ['deps-manager', '--version'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        return False

def containerize_and_run_tests(requirements_file, tests_dir):
    """
    Containerize the project and run tests in a specified directory.
    """

    # Ensure deps-manager is installed
    if not is_deps_manager_installed():
        print("This command requires 'deps-manager' to be installed in the current virtual environment.")
        print("Please install 'deps-manager' by running 'pip install deps-manager' command and try again.")
        return

    # Ensure Docker is installed
    try:
        subprocess.run(
            ['docker', 'version'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError:
        print("Docker is not installed or not running. Please install Docker to proceed.")
        return
    
    # Create a Dockerfile
    dockerfile_content = f"""
    # Base image with Python installed
    FROM python:3.8-slim

    # Set the working directory in the container
    WORKDIR /app

    # Copy the project files into the container
    COPY . /app

    # Install the required dependencies
    RUN pip install -r {requirements_file} && pip install pytest

    # Default command to run the specified test directory
    CMD pytest {tests_dir}
    """

    # Write Dockerfile to a file
    dockerfile_path = "Dockerfile"
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    # Build the Docker container
    build_command = ["docker", "build", "-t", "project_test", "."]
    subprocess.run(build_command, check=True)

    # Run tests in the Docker container
    run_command = ["docker", "run", "--rm", "project_test"]
    subprocess.run(run_command, check=True)

    print("Tests completed in the Docker container.")
