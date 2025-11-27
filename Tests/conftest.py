# content of conftest.py

import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--run-gui", action="store_true", default=False, help="run gui tests"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "gui: mark test as needing a GUI session to run")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-gui"):
        # --run-gui given in cli: do not skip gui tests
        return
    skip_gui = pytest.mark.skip(reason="need --run-gui option to run")
    for item in items:
        if "gui" in item.keywords:
            item.add_marker(skip_gui)
