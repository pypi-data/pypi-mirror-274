import os
import sys
import time
import re
import shutil
from contextlib import redirect_stdout, redirect_stderr
from qualys_tbx.qtbx_policy_merge import policy_merge_01
from qualys_tbx.qtbx_lib import qtbx_lib_config
from qualys_tbx.qtbx_lib import qtbx_lib_functions
from qualys_tbx.qtbx_lib import qtbx_lib_logger
from qualys_tbx.qtbx_lib import qtbx_lib_authentication

tool_list: list[str] = ['policy_merge']


def print_usage(message="", logger_method=print):
    logger_method(message)

    usage = """
    qualystbx --execute policy_merge [options]
    """
    logger_method(usage)


def determine_tool_to_run():
    tool_selected_to_run = None
    for i in range(1, len(sys.argv) - 1):
        if sys.argv[i] == '--execute':
            # Check if there is an argument after '--execute'
            if i + 1 < len(sys.argv):
                next_arg = sys.argv[i + 1]
                # Check if the next argument starts with a letter or digit
                if re.match("^[a-zA-Z0-9]", next_arg):
                    tool_selected_to_run = next_arg
                    break  # Exit the loop after finding and validating '--execute'
                else:
                    print_usage(message="No Tool Selected. Please select tool from options")
                    sys.exit(1)
            else:
                print_usage(
                    message=f"Tool Selected has invalid characters: {tool_selected_to_run}, please select tool from options.")
                sys.exit(1)

    # Optional: Print the tool name if it was found
    if tool_selected_to_run in tool_list:
        return tool_selected_to_run
    else:
        print_usage(message=f"Tool Selected is invalid: {tool_selected_to_run}, please select tool from options.")
        sys.exit(1)


# def determine_storage_dir():
#     # Initialize a variable to hold the word following '--execute'
#     storage_dir = None
#     # Loop through each argument, stopping before the last to avoid IndexError
#     for i in range(1, len(sys.argv) - 1):
#         if sys.argv[i] == '--storage_dir':
#             if i + 1 < len(sys.argv):
#                 next_arg = sys.argv[i + 1]
#                 # Check if the next argument starts with a letter or digit
#                 if re.match(r"^[a-zA-Z0-9\\:_/-]+$", next_arg):
#                     storage_dir = next_arg
#                     break  # Exit the loop after finding and validating '--execute'
#                 else:
#                     print_usage(message="--storage_dir not selected. "
#                                         "Please select a root storage directory. "
#                                         "e.g.:--storage_dir=C:\\users\myname\Downloads")
#                     sys.exit(1)
#             else:
#                 print_usage(message=f"--storage_dir invalid characters: {storage_dir}, please select another --storage_dir=path and rerun")
#                 sys.exit(1)
#     if storage_dir is None:
#         storage_dir = os.path.expanduser('~')
#
#     return storage_dir


def determine_storage_dir():
    # Initialize storage_dir with the user's home directory by default
    storage_dir = os.path.expanduser('~')

    # Loop through each argument, stopping before the last to avoid IndexError
    for i in range(1, len(sys.argv) - 1):
        if sys.argv[i] == '--storage_dir':
            if i + 1 < len(sys.argv):
                next_arg = sys.argv[i + 1]
                # Check if the next argument is a valid file path
                if re.match(r"^[a-zA-Z0-9_ /\\:.-]+$", next_arg):
                    storage_dir = next_arg
                    break  # Exit the loop after finding and validating '--storage_dir'
                else:
                    print_usage(message="Invalid --storage_dir path. "
                                        "Please select a valid root storage directory. "
                                        "e.g.: --storage_dir=C:\\users\\myname\\Downloads or --storage_dir=/home/myname/Downloads")
            else:
                print_usage(message=f"--storage_dir argument is missing a value.")

    print(f"Using storage directory: {storage_dir}")
    return storage_dir


def determine_log_to_console():
    log_to_console = False
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--log_to_console':
            log_to_console = True
    return log_to_console


def qtbx_conflict_check():
    pass
    # matches = qtbx_lib_config.pgrep_af(f"{qtbx_lib_config.qtbx_tool_selected_to_run}")
    # if matches:
    #     print("Conflicting processes found:")
    #     for pid, cmdline in matches:
    #         print(f" - PID: {pid}, Command Line: {cmdline}")
    #     print(f"Error: Conflicting QTBX: {qtbx_lib_config.qtbx_tool_selected_to_run}, running for user: {qtbx_lib_config.qtbx_home_dir}")
    #     print(f"Error: Cannot execute concurrently: {qtbx_lib_config.qtbx_tool_selected_to_run}, running for user: {qtbx_lib_config.qtbx_home_dir}")
    #     print(f"Error: Rerun when after Conflicting ETL completes: {qtbx_lib_config.qtbx_tool_selected_to_run} -> {qtbx_lib_config.qtbx_home_dir}")
    #     exit(1)


def qtbx_execute_tool():
    if qtbx_lib_config.qtbx_tool_selected_to_run == "policy_merge":
        policy_merge_01.main()
    else:
        print_usage(
            message=f"Qualys Toolbox component selected is invalid: {qtbx_lib_config.qtbx_tool_selected_to_run}, please rerun with valid option\n")
        exit(1)

def rotate_log_check(log_file_path=None, log_file_max_size=1000000000, log_file_rotate_path=None):
    if log_file_path.is_file():
        log_file_size = log_file_path.stat().st_size  # In Bytes
        if log_file_size > log_file_max_size:
            shutil.copy2(log_file_path, log_file_rotate_path, follow_symlinks=True)
            fo = open(log_file_path, 'w+')
            fo.close()


# def execute_qualystbx(lock_file=None, log_dir=None, log_file_path=None, log_to_console=True, log_file_rotate_path=None):
#     if log_to_console:
#         qtbx_main()
#     else:
#         try:
#             with open(lock_file, 'wb+') as lock_program_fcntl:  # If locked, exit.
#                 fcntl.flock(lock_program_fcntl, fcntl.LOCK_EX | fcntl.LOCK_NB)
#                 exception_message = "ERROR: rotate_log_check. Please retry later: "
#                 rotate_log_check(log_file_path=log_file_path,
#                                  log_file_max_size=10000000,
#                                  log_file_rotate_path=log_file_rotate_path
#                                  )
#                 if log_dir.is_dir():
#                     exception_message = "ERROR: spawn_etl_in_background. Please retry later: "
#                     with open(log_file_path, 'a', newline='', encoding='utf-8') as log_fo:
#                         with redirect_stdout(log_fo), redirect_stderr(sys.stdout):
#                             qtbx_main()
#                             log_fo.flush()
#                 else:
#                     exception_message = f"ERROR: logdir_missing: {log_dir} - Potential permissions issue."
#                     raise Exception(exception_message)
#
#
#         except Exception as e:
#             print(f"{exception_message} {__file__} ")
#             print(f"Exception: {e}")
#             exit(1)


def execute_qualystbx(lock_file=None, log_dir=None, log_file_path=None, log_to_console=True, log_file_rotate_path=None):
    if log_to_console:
        qtbx_main()
    else:
        exception_message = ""
        try:
            exception_message = "ERROR: rotate_log_check. Please retry later: "
            rotate_log_check(log_file_path=log_file_path,
                             log_file_max_size=10000000,
                             log_file_rotate_path=log_file_rotate_path
                             )
            if log_dir.is_dir():
                exception_message = "ERROR: spawn_etl_in_background. Please retry later: "
                with open(log_file_path, 'a', newline='', encoding='utf-8') as log_fo:
                    with redirect_stdout(log_fo), redirect_stderr(sys.stdout):
                        qtbx_main()
                        log_fo.flush()
            else:
                exception_message = f"ERROR: logdir_missing: {log_dir} - Potential permissions issue."
                raise Exception(exception_message)


        except Exception as e:
            print(f"{exception_message} {__file__} ")
            print(f"Exception: {e}")
            exit(1)


def qtbx_main(logger=print):
    qtbx_lib_logger.setup_logging_stdout(my_logger_prog_name=qtbx_lib_config.qtbx_tool_selected_to_run)
    qtbx_lib_config.log_qtbx_directories()
    qtbx_credentials_dict = qtbx_lib_authentication.get_credentials_from_env()
    qtbx_lib_authentication.get_gateway_platform_fqdn(qtbx_credentials_dict['q_api_fqdn_server'])
    qtbx_lib_authentication.get_qualys_portal_version(
        api_fqdn_server=qtbx_credentials_dict['q_api_fqdn_server'],
        authorization=qtbx_credentials_dict['q_base64_credentials'],
        qtbx_tool='qualystbx',
        message='BEGIN',
    )
    qtbx_execute_tool()
    qtbx_lib_functions.remove_file_safely(file_path=qtbx_lib_config.qtbx_log_file_lock_path, message_hint="lock file", logger=qtbx_lib_logger.logger)

def main():
    qtbx_lib_functions.check_is_admin_or_root()
    qtbx_lib_functions.check_modules_installed(qtbx_lib_functions.required_modules_to_check)
    qtbx_lib_config.qtbx_tool_selected_to_run = determine_tool_to_run()
    qtbx_lib_config.qtbx_storage_dir = determine_storage_dir()
    qtbx_lib_config.qtbx_log_to_console = determine_log_to_console()
    qtbx_lib_config.set_qtbx_directories()
    qtbx_conflict_check()
    qtbx_lib_config.create_qtbx_directories()
    qtbx_lib_config.set_qtbx_log_file_path(f"{qtbx_lib_config.qtbx_tool_selected_to_run}.log")

    execute_qualystbx(
        lock_file=qtbx_lib_config.qtbx_log_file_lock_path,
        log_file_path=qtbx_lib_config.qtbx_log_file_path,
        log_dir=qtbx_lib_config.qtbx_log_dir,
        log_to_console=qtbx_lib_config.qtbx_log_to_console
    )

if __name__ == "__main__":
    main()

    # for i, arg in enumerate(sys.argv[1:], start=1):
    #    print(f"Argument {i}: {arg}")
    # qtbx_lib.qtbx_lib_config.create_qtbx_directories()
    # qtbx_lib_functionscreate_local_directory("data")
    # args = get_args()
    # merge_policies()
    # export_policy()
    # q_dict : dict = prepare_export_policy_id_api_call()
    # policy_dict, policy_str = read_xml(q_dict)
    # policy_dict_updated = get_control_list_from_policy(policy_dict, ['9705', '9712'])
    # write_xml(q_dict, policy_dict_updated)
    # write_json(q_dict, policy_dict_updated)
    # policy_dict = read_xml_with_cdata("data/export_policy_id_2661242_results_file.xml")
    # write_xml_with_cdata(policy_dict, "data/export_policy_id_2661242_results.xml")
