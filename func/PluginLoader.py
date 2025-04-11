import builtins
import importlib.util
import inspect
import sys
import os
import types


class ModulePrint:
    def __init__(self):
        self._original_stdout = sys.stdout

    def write(self, message: str):
        if message.strip() == '':
            self._original_stdout.write("\n")
            return
        caller_module = inspect.stack()[2]
        module_name = caller_module.filename.split("\\")[-1].split(".")[0]
        self._original_stdout.write(f"[{module_name}] {message}")

    def flush(self):
        self._original_stdout.flush()


class DynamicImporter:
    def __init__(self, module_name, file_path, globals_dict, allowed_modules):
        self.module_name = module_name
        self.file_path = file_path
        self.globals_dict = globals_dict
        self.allowed_modules = allowed_modules

    def restricted_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith('.') or len(name.split(".")) == level:
            return self.original_import(name, globals, locals, fromlist, level)
        if name.split('.')[0] not in self.allowed_modules and not name in self.allowed_modules:
            raise ImportError(f"Import of module '{name}' is not allowed")
        return self.original_import(name, globals, locals, fromlist, level)

    def print(self, *argv, **kwargs):
        print(*argv, **kwargs)

    def load_module(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"file {self.file_path} not found!")

        for name, module in self.globals_dict.items():
            if isinstance(module, types.ModuleType):
                sys.modules[name] = module

        file_abs_path = os.path.abspath(self.file_path)
        spec = importlib.util.spec_from_file_location(self.module_name, file_abs_path)
        module = importlib.util.module_from_spec(spec)

        module_dir = os.path.dirname(self.file_path)
        package_name = os.path.basename(os.path.dirname(module_dir)) + '.' + os.path.basename(module_dir)

        module.__file__ = self.file_path
        module.__package__ = package_name
        module.__path__ = [module_dir]

        self.original_import = builtins.__import__
        builtins.__import__ = self.restricted_import

        try:
            self.globals_dict['print'] = self.print
            module.__dict__.update(self.globals_dict)
            sys.modules[self.module_name] = module
            spec.loader.exec_module(module)
            self.globals_dict.update(module.__dict__)
        finally:
            builtins.__import__ = self.original_import

        return module

