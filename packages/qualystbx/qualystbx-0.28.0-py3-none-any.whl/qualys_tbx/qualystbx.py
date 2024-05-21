import os
import subprocess
import sys
import venv
import traceback
import urllib
import re
from pathlib import Path
from datetime import datetime
from contextlib import redirect_stdout, redirect_stderr

from qualys_tbx import qualystbx_main
from qualys_tbx.qtbx_lib import qtbx_lib_config
from qualys_tbx.qtbx_lib import qtbx_lib_functions
from qualys_tbx.qtbx_lib import qtbx_lib_logger
from qualys_tbx.qtbx_lib import qtbx_lib_authentication


def prepare_for_logging(multiline_string):
    lines = multiline_string.splitlines()
    pattern = re.compile(r'[^\x20-\x7E]+|\|')
    cleaned_lines = [pattern.sub('', line) for line in lines]
    return cleaned_lines

def run_subprocess(command, shell=True, check=False, executable=None):
    """Runs a subprocess and captures stdout, stderr, and other details in a dictionary."""

    if executable is None:
        result = subprocess.run(command, shell=shell, check=check,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:

        result = subprocess.run(command, shell=shell, check=check, executable=executable,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode().strip()
    stdout = prepare_for_logging(stdout)
    stderr = result.stderr.decode().strip()
    stderr = prepare_for_logging(stderr)
    return {
        'command': command,
        'returncode': result.returncode,
        'stdout': stdout,
        'stderr': stderr
    }


def create_virtualenv(env_name, rebuild=False):
    """Creates a virtual environment if it doesn't already exist."""
    if not os.path.exists(env_name) or rebuild is True:
        if rebuild is True:
            qtbx_lib_logger.logger_info(f"Rebuilding virtual environment in {env_name}...")
        else:
            qtbx_lib_logger.logger_info(f"Creating virtual environment in {env_name}...")

        try:
            venv.create(env_name, with_pip=False)
        except subprocess.CalledProcessError as e:
            qtbx_lib_logger.logger_error(f"Error creating virtual environment with pip: {e}")
            exit(1)
    else:
        qtbx_lib_logger.logger_info(f"Virtual environment {env_name} already exists.")


def bootstrap_pip(env_name):
    """Bootstraps pip in the virtual environment."""
    activate_script = activate_virtualenv(env_name)
    get_pip_script = os.path.join(env_name, 'get-pip.py')

    qtbx_lib_logger.logger_info("Downloading get-pip.py...")
    url = 'https://bootstrap.pypa.io/get-pip.py'
    try:
        with urllib.request.urlopen(url) as response:
            with open(get_pip_script, 'wb') as file:
                file.write(response.read())
        qtbx_lib_logger.logger_info("Downloaded get-pip.py successfully.")
    except Exception as e:
        qtbx_lib_logger.logger_error(f"Failed to download get-pip.py: {e}")
        exit(1)

    qtbx_lib_logger.logger_info("Installing pip...")
    if os.name == 'nt':
        command = f'{activate_script} && python {get_pip_script}'
        result = run_subprocess(command, check=True)
    else:
        command = f'source {activate_script} && python {get_pip_script}'
        result = run_subprocess(command, check=True, executable='/bin/bash')

    [qtbx_lib_logger.logger_info(f"pip install - {line}") for line in result['stdout']]
    if result['returncode'] != 0:
        [qtbx_lib_logger.logger_error(f"pip install - {line}") for line in result['stderr']]
        exit(1)

    qtbx_lib_logger.logger_info("Cleaning up get-pip.py...")
    os.remove(get_pip_script)


def is_module_installed(env_name, module):
    """Checks if a module is installed in the virtual environment."""
    activate_script = activate_virtualenv(env_name)
    if os.name == 'nt':
        command = f'{activate_script} && python -c "import {module}"'
        result = run_subprocess(command)
    else:
        command = f'source {activate_script} && python -c "import {module}"'
        result = run_subprocess(command, check=False, executable='/bin/bash')

    if result['returncode'] != 0:
        [qtbx_lib_logger.logger_warning(f"module not installed: {module} - {line}") for line in result['stderr']]
    return result['returncode'] == 0


def install_modules(env_name, modules):
    """Installs a list of modules into the virtual environment if they are not already installed."""
    modules_to_install = [module for module in modules if not is_module_installed(env_name, module)]

    if modules_to_install:
        modules_command = ' '.join(modules_to_install)
        qtbx_lib_logger.logger_info(f"Installing modules: {modules_command}")
        if os.name == 'nt':
            command = f'{activate_virtualenv(env_name)} && pip install --force-reinstall {modules_command}'
            result = run_subprocess(command, check=True)
        else:
            command = f'source {activate_virtualenv(env_name)} && pip install --force-reinstall {modules_command}'
            result = run_subprocess(command, check=True, executable='/bin/bash')

        [qtbx_lib_logger.logger_info(f"module install - {line}") for line in result['stdout']]
        if result['returncode'] != 0:
            [qtbx_lib_logger.logger_error(f"error module install - {line}") for line in result['stderr']]
    else:
        qtbx_lib_logger.logger_info("All modules are already installed.")


def test_virtualenv(env_name):
    """Tests if the virtual environment is working correctly."""
    try:
        activate_script = activate_virtualenv(env_name)
        test_command = 'python -c "import sys; print(sys.executable)"'

        if os.name == 'nt':
            command = f'{activate_script} && {test_command}'
            result = run_subprocess(command)
        else:
            command = f'source {activate_script} && {test_command}'
            result = run_subprocess(command, check=True, executable='/bin/bash')

        if result['returncode'] == 0:
            [qtbx_lib_logger.logger_info(f"{line}") for line in result['stdout']]
        else:
            [qtbx_lib_logger.logger_warning(f"{line}") for line in result['stdout']]
        return result['returncode'] == 0
    except Exception as e:
        return 1


def rename_virtualenv(env_name):
    """Renames the existing virtual environment directory by appending a timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_name = f"{env_name}_oldvenv_{timestamp}"
    os.rename(env_name, new_name)
    qtbx_lib_logger.logger_info(f"Renamed existing virtual environment to {new_name}")


def recreate_virtualenv(env_name, modules):
    """Recreates the virtual environment if it fails the test."""
    qtbx_lib_logger.logger_info(f"Recreating virtual environment in {env_name}...")
    # Rename the existing virtual environment
    if os.path.exists(env_name):
        rename_virtualenv(env_name)

    # Create a new virtual environment
    create_virtualenv(env_name, rebuild=True)
    # Bootstrap pip in the new virtual environment
    try:
        bootstrap_pip(env_name)
    except subprocess.CalledProcessError as e:
        qtbx_lib_logger.logger_error(f"Error bootstrapping pip: {e}")
        exit(1)

    try:
        install_modules(env_name, modules)
    except subprocess.CalledProcessError as e:
        qtbx_lib_logger.logger_error(f"Error installing modules: {e}")
        exit(1)

def run_module_in_virtualenv(env_name, module_name, module_args):
    activate_script = activate_virtualenv(env_name)
    module_command = f'python -m {module_name} ' + ' '.join(module_args)
    try:
        if os.name == 'nt':
            command = f'{activate_script} && {module_command}'
            qtbx_lib_logger.logger_info(f"Executing {command}")
            result = subprocess.run(command, shell=True)
        else:
            command = f'source {activate_script} && {module_command}'
            qtbx_lib_logger.logger_info(f"Executing {command}")
            result = subprocess.run(command, shell=True, executable='/bin/bash')
        result.check_returncode()
    except subprocess.CalledProcessError as e:
        qtbx_lib_logger.logger_error(f"Error: Command '{e.cmd}' returned non-zero exit status {e.returncode}")
        exit(1)
    except Exception as e:
        qtbx_lib_logger.logger_error(f"An unexpected error occurred: {e}")
        exit(1)

def activate_virtualenv(env_name):
    """Returns the path to the activation script of the virtual environment."""
    if os.name == 'nt':
        return os.path.join(env_name, 'Scripts', 'activate')
    else:
        return os.path.join(env_name, 'bin', 'activate')


def run_module_in_virtualenv_new(env_name, module_name, module_args):
    activate_script = activate_virtualenv(env_name)
    module_command = [sys.executable, '-m', module_name] + module_args
    try:
        if os.name == 'nt':
            command = f'{activate_script} && ' + ' '.join(module_command)
            subprocess.run(command, shell=True)
        else:
            command = ['bash', '-c', f'source {activate_script} && ' + ' '.join(module_command)]
            qtbx_lib_logger.logger_info(f"Executing {command}")
            result = subprocess.run(command, executable='/bin/bash')
            result.check_returncode()
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{e.cmd}' returned non-zero exit status {e.returncode}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

def qtbx_main():
    qtbx_lib_functions.check_is_admin_or_root()
    qtbx_lib_functions.check_modules_installed(qtbx_lib_functions.required_modules_to_check)
    qtbx_lib_config.qtbx_tool_selected_to_run = qualystbx_main.determine_tool_to_run()
    qtbx_lib_config.qtbx_storage_dir = qualystbx_main.determine_storage_dir()
    qtbx_lib_config.qtbx_log_to_console = qualystbx_main.determine_log_to_console()
    qtbx_lib_config.qtbx_rebuild_venv = qualystbx_main.determine_rebuild_venv()
    qtbx_lib_config.set_qtbx_directories()
    qtbx_lib_config.create_qtbx_directories()
    qtbx_lib_config.set_qtbx_log_file_path(f"{qtbx_lib_config.qtbx_tool_selected_to_run}.log")
    qtbx_lib_logger.setup_logging(log_file_path=qtbx_lib_config.qtbx_log_file_path, my_logger_prog_name=f"venv_setup_{qtbx_lib_config.qtbx_tool_selected_to_run}", log_to_console=qtbx_lib_config.qtbx_log_to_console)
    qtbx_lib_config.log_qtbx_directories()
    env_name = Path(qtbx_lib_config.qtbx_venv_dir)
    script_name = 'qualystbx_main'  # The console script to run
    script_args = sys.argv[1:]
    module_name = 'qualystbx_main'
    module_args = sys.argv[1:]

    modules = ['qualystbx', 'requests', 'lxml', 'psutil', 'xmltodict', 'qualystbx',]
    if not test_virtualenv(env_name) or qtbx_lib_config.qtbx_rebuild_venv is True:
        qtbx_lib_logger.logger_info(f"Virtual environment {env_name} is being rebuilt.")
        recreate_virtualenv(env_name, modules)
    result = run_module_in_virtualenv(env_name, module_name, module_args)
    qtbx_lib_logger.logger_info(f"End QualysTBX")

def main():
    try:
        qtbx_main()
    except Exception as e:
        print(f"ERROR: {e}")
        formatted_lines = traceback.format_exc().splitlines()
        print(f"ERROR: {formatted_lines}")


if __name__ == '__main__':
        main()


# def run_console_script_in_virtualenv(env_name, script_name, script_args):
#     """Runs a console script inside the virtual environment."""
#     activate_script = activate_virtualenv(env_name)
#
#     # Combine script name and script arguments into one command
#     script_command = f'{script_name} ' + ' '.join(script_args)
#
#     if os.name == 'nt':
#         command = f'{activate_script} && {script_command}'
#     else:
#         command = f'source {activate_script} && {script_command}'
#
#     result = run_subprocess(command, executable='/bin/bash')
#
#     print(result['stdout'])
#     if result['returncode'] != 0:
#         print(result['stderr'])


# def run_console_script_in_virtualenv(env_name, script_name, script_args):
#     """Runs a console script inside the virtual environment."""
#     activate_script = activate_virtualenv(env_name)
#
#     # Combine script name and script arguments into one command
#     script_command = f'{script_name} ' + ' '.join(script_args)
#
#     if os.name == 'nt':
#         command = f'{activate_script} && {script_command}'
#         subprocess.run(command, shell=True)
#     else:
#         command = f'source {activate_script} && {script_command}'
#         subprocess.run(command, shell=True, executable='/bin/bash')
#

# def activate_virtualenv(env_name):
#     """Returns the path to the activation script of the virtual environment."""
#     if os.name == 'nt':
#         activate_script = os.path.join(env_name, 'Scripts', 'activate.bat')
#     else:
#         activate_script = os.path.join(env_name, 'bin', 'activate')
#
#     return activate_scrip