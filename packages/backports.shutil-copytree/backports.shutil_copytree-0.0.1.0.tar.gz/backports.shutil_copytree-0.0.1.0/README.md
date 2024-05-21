## backports.shutil_copytree

### Usage

```py
try:
    from inspect import signature
except ImportError:
    try:
        from funcsigs import signature
    except ImportError:
        signature = None

from shutil import copytree
if 'dirs_exist_ok' not in signature(copytree).parameters:
    from backports.shutil_copytree import copytree
```

### Caveats

- symlink stat is not copied when Python<3.3
- directory junctions check on Windows Python<3.8 is done via pywin32, which is less-tested.
