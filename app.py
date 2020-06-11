import sys
import os
import re


def is_python_file(file_name):
    if re.match(".*\.py$", file_name):
        return True

    return False


def recursive_search(dir_path, python_files):
    # list all files in the current directory
    files = os.listdir(dir_path)

    for file_name in files:
        full_path = os.path.join(dir_path, file_name)

        if os.path.isdir(full_path):
            recursive_search(full_path, python_files)
        elif os.path.isfile(full_path):
            if is_python_file(full_path):
                python_files.append(full_path)

                print("Python file {file_path} appended".format(
                    file_path=full_path
                ))
            else:
                print("Not a python file, passed.")
        else:
            print("Not a file or directory, passed.")


def scan_modules(file_path):
    modules = set()

    from_pattern = "[\^\n] *from\s+(\w+)"
    import_pattern = "[\^\n] *import\s+(\w+)"

    with open(file_path) as f:
        data = f.read()

        modules |= set(re.findall(from_pattern, data))
        modules |= set(re.findall(import_pattern, data))

    return modules


if __name__ == "__main__":
    root_path = "/Users/yua/Documents/Projects/RSB2-Forked"
    python_files = []
    modules = set()

    print("-" * 10 + "Scanning python files..." + "-" * 10)

    recursive_search(root_path, python_files)

    print("-" * 10 + "Scanning modules..." + "-" * 10)
    
    for python_file in python_files:
        modules |= scan_modules(python_file)

    print(modules)
