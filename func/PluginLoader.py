import importlib.util
import sys
import os
import types


class DynamicImporter:
    def __init__(self, module_name, file_path, globals_dict):
        self.module_name = module_name
        self.file_path = file_path
        self.globals_dict = globals_dict

    def load_module(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"file {self.file_path} not found!")

        for name, module in self.globals_dict.items():
            if isinstance(module, types.ModuleType):
                sys.modules[name] = module

        file_abs_path = os.path.abspath(self.file_path)
        spec = importlib.util.spec_from_file_location(self.module_name, file_abs_path)
        module = importlib.util.module_from_spec(spec)
        file_abs_path = os.path.abspath(self.file_path)
        module_dir = os.path.dirname(self.file_path)
        package_name = os.path.basename(os.path.dirname(module_dir)) + '.' + os.path.basename(module_dir)
        module.__file__ = self.file_path
        module.__package__ = package_name
        module.__path__ = [module_dir]
        module.__dict__.update(self.globals_dict)
        sys.modules[self.module_name] = module
        spec.loader.exec_module(module)
        self.globals_dict.update(module.__dict__)
        return module

