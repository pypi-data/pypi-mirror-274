# ensurepkg

`ensurepkg` is a minimal package to ensure a pip-managed package exists.

# example

```example.py
from ensurepkg import EnsurePkg

for guard in EnsurePkg(dict(dotenv="python-dotenv")):
    with guard:
        import dotenv

with EnsurePkg(dict(git="GitPython"), cache_dir="/tmp/ensurepkg"):
    import git

print(dotenv.__name__)
print(git.__name__, git.__version__)
```

# cache_dir

`cache_dir` is where ensurepkg installs the packages. It is isolated from other environments and it's resolved as:

1. setting programatically via `EnsurePkg(cache_dir="...")`
2. from env var $ENSUREPKG_DIR
3. from env var $XDG_CACHE_HOME/ensurepkg
4. from env var $HOME/.cache/ensurepkg
5. /tmp/ensurepkg