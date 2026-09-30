import sys

import pytest


TEST_GROUPS = {"smoke", "search", "product", "cart"}


def main() -> int:
    arguments = sys.argv[1:]
    if arguments and arguments[0].lower() in TEST_GROUPS:
        marker = arguments.pop(0).lower()
        arguments = ["-m", marker, *arguments]
    return pytest.main(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
