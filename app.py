import sys
import os
import re
import importlib
from utils import is_python_file
from config import PROJECT_PATH, REG_PATTERN


def recursive_search(dir_path, python_files, python_file_names):
    # list all files in the current directory
    files = os.listdir(dir_path)

    for file_name in files:
        full_path = os.path.join(dir_path, file_name)

        if os.path.isdir(full_path):
            recursive_search(full_path, python_files, python_file_names)
        elif os.path.isfile(full_path):
            if is_python_file(file_name):
                python_file_names.append(file_name[:-3])
                python_files.append(full_path)

                # print("Python file {file_path} appended".format(
                #     file_path=file_name
                # ))
            else:
                pass
                # print("Not a python file, passed.")
        else:
            pass
            # print("Not a file or directory, passed.")


def scan_modules(file_path):
    modules = set()

    with open(file_path) as f:
        data = f.read()

        modules |= set(re.findall(REG_PATTERN["python_import"], data, re.S))
        modules |= set(re.findall(REG_PATTERN["python_from_import"], data, re.S))

    return modules


def create_req_list_file(modules):
    if isinstance(modules, list):
        modules = "\n".join(modules)

        with open(os.path.join(PROJECT_PATH, "requirements.txt")) as f:
            f.write(modules)

        return True
    return False


if __name__ == "__main__":
    python_files = []
    python_file_names = []
    modules = set()

    print("Scanning python files...")

    recursive_search(PROJECT_PATH, python_files, python_file_names)

    print("Found {0} python files, scanning modules...".format(
        len(python_file_names)
    ))

    for python_file in python_files:
        modules |= scan_modules(python_file)

    handled_modules = []

    for module in modules:
        try:
            importlib.find_module(module)
        except Exception as e:
            handled_modules.append(module)
            continue

    print("Modules not installed:")
    print(handled_modules)


