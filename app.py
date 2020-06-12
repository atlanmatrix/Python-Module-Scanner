import sys
import os
import re
import importlib
from importlib import util
from utils import is_python_file
from config import PROJECT_PATH, REG_PATTERN


def create_req_list_file(modules):
    if isinstance(modules, list):
        modules = "\n".join(modules)

        with open(os.path.join(PROJECT_PATH, "requirements.txt")) as f:
            f.write(modules)

        return True
    return False


class Application:
    def __init__(self):
        super().__init__()

        self.args = []
        self.handler()
        
    def handler(self):
        self.args = sys.argv

        if len(self.args) == 1:
            self._show_uninstalled_modules()
        elif len(self.args) >= 2:
            if self.args[1] == "export":
                self._export_modules()
            elif self.args[1] == "import":
                self._import_modules()
            elif self.args[1] == "clean":
                self._clean_modules()

    def _pyfile_searcher(self, dir_path=PROJECT_PATH, pyfiles=[], pyfile_names=[]):
        files = os.listdir(dir_path)

        for file_name in files:
            full_path = os.path.join(dir_path, file_name)

            if os.path.isdir(full_path):
                pyfiles, pyfile_names = self._pyfile_searcher(full_path, 
                                                        pyfiles, pyfile_names)

            elif os.path.isfile(full_path):
                if is_python_file(file_name):
                    pyfile_names.append(file_name[:-3])
                    pyfiles.append(full_path)
                else:
                    pass
            else:
                pass

        return pyfiles, pyfile_names

    def _modules_analyzer(self):
        modules = set()

        print("[Scanning python files...]")

        _pyfiles, _pyfile_names = self._pyfile_searcher()

        print("[Found \033[0;32;40m{0}\033[0m python files, "
                "scanning modules...]".format(
            len(_pyfile_names)
        ))

        for pyfile in _pyfiles:
            modules |= self._module_scanner(pyfile)

        return [m for m in modules if m not in _pyfile_names]

    def _module_scanner(self, file_path):
        modules = set()

        with open(file_path) as f:
            data = f.read()

            modules |= set(re.findall(REG_PATTERN["python_import"], data, re.S))
            modules |= set(re.findall(REG_PATTERN["python_from_import"], data, re.S))

        return modules

    def _show_uninstalled_modules(self):
        raw_modules = self._modules_analyzer()

        uninstalled_modules = []

        for module in raw_modules:
            r = util.find_spec(module)
            
            if r is None:
                uninstalled_modules.append(module)
                continue

        print("\033[0;32;40m[Modules not installed:]\033[0m \n{0}".format(
            "\n".join(uninstalled_modules)
        ))

    def _clean_modules(self):
        raw_modules = self._modules_analyzer()

        export_name = "requirements.txt"
        useful_modules = []

        if len(self.args) == 3:
            export_name = self.args[2]

        target_file_name = os.path.join(PROJECT_PATH, export_name)

        with open(target_file_name) as f:
            data = f.read()

            modules = data.split("\n")

            for module in modules:
                module_name = module.split("==")[0]
                
                if module_name in raw_modules:
                    useful_modules.append(module)

            with open(target_file_name, "w") as f:
                f.write("\n".join(useful_modules))



    def _export_modules(self):
        raw_modules = self._modules_analyzer()

        modules_need_export = []

        for module_name in raw_modules:
            try:
                # exists module will set version
                m = importlib.import_module(module_name)
                module_version = m.__version__
                modules_need_export.append("{m_name}=={m_version}".format(
                    m_name=module_name, 
                    m_version=module_version
                ))
            except Exception as e:
                # module not exists or no version found will not set version
                modules_need_export.append(module_name)

        export_name = "requirements.txt"

        if len(self.args) == 3:
            export_name = self.args[2]

        target_file_name = os.path.join(PROJECT_PATH, export_name)
        
        with open(target_file_name, "w") as f:
            f.write("\n".join(modules_need_export))
            f.close()

            print("\033[0;32;40m[Export successfully]\033[0m {0}".format(
                target_file_name
            ))

    def _import_modules(self):
        pass


if __name__ == "__main__":
    Application()
