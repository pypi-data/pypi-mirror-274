import sys
from os import environ as env, execvpe as os_exec
from importlib import invalidate_caches as reload_path
from subprocess import run


__version__ = '0.1.0'
__all__ = ["EnsurePkg"]


CACHE_DIR=env.get("ENSUREPKG_DIR", env.get("XDG_CACHE_HOME", env.get["HOME"] + "/.cache" if "HOME" in env else "/tmp") + "/ensurepkg")
PYTHON=sys.executable if sys.executable else "python"
PIP_INSTALL=[PYTHON, "-m", "pip", "install", "-t"]


class EnsurePkg:
    def __init__(
            self,
            pkg_mapping,
            cache_dir = CACHE_DIR,
            incremental = False,
    ):
        self.mapping = pkg_mapping
        self.cache_dir = cache_dir
        self.passed = False
        self.incremental = incremental
        self.syspath_start_index = None

    def __enter__(self):
        self.syspath_start_index = len(sys.path)
        sys.path.append(self.cache_dir)

    def __exit__(self, _exc_type, exc_value, _traceback):
        sys.path.pop(self.syspath_start_index + sys.path[self.syspath_start_index:].index(self.cache_dir))
        if isinstance(exc_value, ModuleNotFoundError):
            module_name = exc_value.name
            if module_name not in self.mapping:
                return False
            if self.incremental:
                run([*PIP_INSTALL, self.cache_dir, self.mapping[module_name]])
                reload_path()
                return True
            else:
                run([*PIP_INSTALL, self.cache_dir, *self.mapping.values()])
                os_exec(PYTHON, [PYTHON, *sys.argv], env)
                # never reached
        elif exc_value is not None:
            return False
        else:
            self.passed = True

    def __iter__(self):
        cls = type(self)
        return cls(self.mapping, cache_dir=self.cache_dir, incremental=True)

    def __next__(self):
        if not self.incremental:
            raise ValueError("Do not call next() directly. __next__ should be called implictly with `for guard in EnsurePkg(...):`")
        if self.passed:
            raise StopIteration
        else:
            return self
            
