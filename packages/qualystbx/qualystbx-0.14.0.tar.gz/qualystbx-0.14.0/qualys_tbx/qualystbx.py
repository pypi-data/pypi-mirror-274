import os
import subprocess
import sys
import venv
import re
from pathlib import Path
from datetime import datetime
from qualys_tbx import qualystbx_main
from qualys_tbx.qtbx_lib import qtbx_lib_config
from qualys_tbx.qtbx_lib import qtbx_lib_functions
from qualys_tbx.qtbx_lib import qtbx_lib_logger
from qualys_tbx.qtbx_lib import qtbx_lib_authentication


def create_virtualenv(env_name):
    """Creates a virtual environment if it doesn't already exist."""
    if not os.path.exists(env_name):
        print(f"Creating virtual environment in {env_name}...")
        venv.create(env_name, with_pip=True)
    else:
        print(f"Virtual environment {env_name} already exists.")


def activate_virtualenv(env_name):
    """Returns the path to the activation script of the virtual environment."""
    if os.name == 'nt':
        activate_script = os.path.join(env_name, 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join(env_name, 'bin', 'activate')

    return activate_script


def bootstrap_pip(env_name):
    """Bootstraps pip in the virtual environment."""
    activate_script = activate_virtualenv(env_name)
    get_pip_script = os.path.join(env_name, 'get-pip.py')

    print("Downloading get-pip.py...")
    subprocess.run(f'curl https://bootstrap.pypa.io/get-pip.py -o {get_pip_script}', shell=True, check=True)

    print("Installing pip...")
    if os.name == 'nt':
        command = f'{activate_script} && python {get_pip_script}'
        subprocess.run(command, shell=True, check=True)
    else:
        command = f'source {activate_script} && python {get_pip_script}'
        subprocess.run(command, shell=True, executable='/bin/bash', check=True)

    print("Cleaning up get-pip.py...")
    os.remove(get_pip_script)


def is_module_installed(env_name, module):
    """Checks if a module is installed in the virtual environment."""
    activate_script = activate_virtualenv(env_name)
    if os.name == 'nt':
        command = f'{activate_script} && python -c "import {module}"'
    else:
        command = f'source {activate_script} && python -c "import {module}"'

    #result = subprocess.run(command, shell=True)
    result = subprocess.run(command, shell=True, executable='/bin/bash')
    return result.returncode == 0


def install_modules(env_name, modules):
    """Installs a list of modules into the virtual environment if they are not already installed."""
    activate_script = activate_virtualenv(env_name)
    modules_to_install = [module for module in modules if not is_module_installed(env_name, module)]

    if modules_to_install:
        modules_command = ' '.join(modules_to_install)
        print(f"Installing modules: {modules_command}")
        if os.name == 'nt':
            command = f'{activate_script} && pip install {modules_command}'
            subprocess.run(command, shell=True, check=True)
        else:
            command = f'source {activate_script} && pip install {modules_command}'
            subprocess.run(command, shell=True, executable='/bin/bash', check=True)
    else:
        print("All modules are already installed.")


def test_virtualenv(env_name):
    """Tests if the virtual environment is working correctly."""
    activate_script = activate_virtualenv(env_name)
    test_command = 'python -c "import sys; print(sys.executable)"'

    if os.name == 'nt':
        command = f'{activate_script} && {test_command}'
        result = subprocess.run(command, shell=True)
    else:
        command = f'source {activate_script} && {test_command}'
        result = subprocess.run(command, shell=True, executable='/bin/bash')

    return result.returncode == 0


def rename_virtualenv(env_name):
    """Renames the existing virtual environment directory by appending a timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_name = f"{env_name}_oldvenv_{timestamp}"
    os.rename(env_name, new_name)
    print(f"Renamed existing virtual environment to {new_name}")


def recreate_virtualenv(env_name, modules):
    """Recreates the virtual environment if it fails the test."""
    print(f"Recreating virtual environment in {env_name}...")
    # Rename the existing virtual environment
    if os.path.exists(env_name):
        rename_virtualenv(env_name)

    # Create a new virtual environment
    create_virtualenv(env_name)
    # Bootstrap pip in the new virtual environment
    try:
        bootstrap_pip(env_name)
        install_modules(env_name, modules)
    except subprocess.CalledProcessError as e:
        print(f"Error bootstrapping pip or installing modules: {e}")
        print("Retrying the creation of the virtual environment...")
        rename_virtualenv(env_name)
        create_virtualenv(env_name)
        bootstrap_pip(env_name)
        install_modules(env_name, modules)


def run_console_script_in_virtualenv(env_name, script_name, script_args):
    """Runs a console script inside the virtual environment."""
    activate_script = activate_virtualenv(env_name)

    # Combine script name and script arguments into one command
    script_command = f'{script_name} ' + ' '.join(script_args)

    if os.name == 'nt':
        command = f'{activate_script} && {script_command}'
        subprocess.run(command, shell=True)
    else:
        command = f'source {activate_script} && {script_command}'
        subprocess.run(command, shell=True, executable='/bin/bash')


def main():
    qtbx_lib_functions.check_is_admin_or_root()
    qtbx_lib_functions.check_modules_installed(qtbx_lib_functions.required_modules_to_check)
    qtbx_lib_config.qtbx_tool_selected_to_run = qualystbx_main.determine_tool_to_run()
    qtbx_lib_config.qtbx_storage_dir = qualystbx_main.determine_storage_dir()
    qtbx_lib_config.qtbx_log_to_console = qualystbx_main.determine_log_to_console()
    qtbx_lib_config.qtbx_rebuild_venv = qualystbx_main.determine_rebuild_venv()
    qtbx_lib_config.set_qtbx_directories()
    qtbx_lib_config.create_qtbx_directories()
    qtbx_lib_config.set_qtbx_log_file_path(f"{qtbx_lib_config.qtbx_tool_selected_to_run}.log")
    if qtbx_lib_config.qtbx_log_to_console is False:
        print(f"See your log file for progress at: {qtbx_lib_config.qtbx_log_file_path}")

    env_name = Path(qtbx_lib_config.qtbx_venv_dir)
    script_name = 'qualystbx_main'  # The console script to run
    script_args = sys.argv[1:]

    modules = ['requests', 'lxml', 'psutil', 'xmltodict', 'qualystbx']
    # Create virtual environment if it doesn't exist
    create_virtualenv(env_name)
    # Test the virtual environment
    if not test_virtualenv(env_name) or qtbx_lib_config.qtbx_rebuild_venv is True:
        print(f"Virtual environment {env_name} is being rebuilt.")
        recreate_virtualenv(env_name, modules)
    else:
        # Install required modules
        install_modules(env_name, modules)

    run_console_script_in_virtualenv(env_name, script_name, script_args)


if __name__ == '__main__':
    main()