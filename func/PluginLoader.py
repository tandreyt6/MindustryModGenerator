import importlib.util
import sys
import os

class DynamicImporter:
    def __init__(self, module_name, file_path, globals_dict):
        self.module_name = module_name
        self.file_path = file_path
        self.globals_dict = globals_dict

    def load_module(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Файл {self.file_path} не найден.")

        file_abs_path = os.path.abspath(self.file_path)

        spec = importlib.util.spec_from_file_location(self.module_name, file_abs_path)
        module = importlib.util.module_from_spec(spec)

        file_abs_path = os.path.abspath(self.file_path)

        module_dir = os.path.dirname(file_abs_path)

        package_name = os.path.basename(os.path.dirname(module_dir)) + '.' + os.path.basename(module_dir)

        module.__package__ = package_name

        module.__path__ = [module_dir]

        sys.modules[self.module_name] = module

        module.__dict__.update(self.globals_dict)

        spec.loader.exec_module(module)

        self.globals_dict.update(module.__dict__)


        return module