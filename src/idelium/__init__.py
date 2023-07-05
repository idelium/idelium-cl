from typing import List, Optional
import sys


__version__ = "23.1.2"


def main(args: Optional[List[str]] = None) -> int:
    """This is an internal API only meant for use by pip's own console scripts.

    For additional details, see https://github.com/pypa/pip/issues/7498.
    """
    from idelium._internal.main import main as _main

    sys.exit(_main())
