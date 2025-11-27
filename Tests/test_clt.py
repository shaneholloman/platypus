#!/usr/bin/env python3

"""
Tests for the Platypus command-line tool.

This test suite uses pytest to verify the functionality of the 'platypus'
command-line tool. It covers profile generation, app creation, and basic
app execution.

To run tests without launching the GUI application:
    pytest

To run tests including the GUI application tests:
    pytest --run-gui
"""

import os
import re
import subprocess
import plistlib
import shutil
from pathlib import Path
from typing import List, Dict, Any, Union

import pytest

# Path to the command-line tool binary
CLT_BINARY = Path(__file__).parent / ".." / "products" / "platypus_clt"
SCRIPTEXEC_BINARY = (
    Path(__file__).parent
    / ".."
    / "products"
    / "ScriptExec.app"
    / "Contents"
    / "MacOS"
    / "ScriptExec"
)
NIB_PATH = (
    Path(__file__).parent
    / ".."
    / "products"
    / "ScriptExec.app"
    / "Contents"
    / "Resources"
    / "MainMenu.nib"
)
TEST_APP_NAME = "TestPlatypusApp"
TEST_APP_PATH = Path(__file__).parent / f"{TEST_APP_NAME}.app"
ARGS_SCRIPT_PATH = Path(__file__).parent / "args.py"
DUMMY_ICON_PATH = Path(__file__).parent / "dummy.icns"
ARGS_OUT_FILE = Path(__file__).parent / "args.txt"


assert CLT_BINARY.exists(), (
    "Platypus command-line tool binary not found at path {}".format(CLT_BINARY)
)
assert SCRIPTEXEC_BINARY.exists(), "ScriptExec binary not found at path {}".format(
    SCRIPTEXEC_BINARY
)
assert NIB_PATH.exists(), "NIB file not found at path {}".format(NIB_PATH)
assert ARGS_SCRIPT_PATH.exists(), "Args script not found at path {}".format(
    ARGS_SCRIPT_PATH
)
assert DUMMY_ICON_PATH.exists(), "Dummy icon not found at path {}".format(
    DUMMY_ICON_PATH
)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    """Set up test environment and clean up after tests."""
    # Change to the directory where the script is located
    os.chdir(Path(__file__).parent)

    # Create dummy files for testing
    Path("dummy1").touch()
    Path("dummy2").touch()

    yield

    # Teardown: Clean up generated files
    if TEST_APP_PATH.exists():
        shutil.rmtree(TEST_APP_PATH)
    if ARGS_OUT_FILE.exists():
        ARGS_OUT_FILE.unlink()
    Path("dummy1").unlink()
    Path("dummy2").unlink()


def get_profile_plist_for_args(args: List[str]) -> Dict[str, Any]:
    """Generate a profile plist from command-line arguments."""
    cmd = [str(CLT_BINARY), *args, "-O", "-"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return plistlib.loads(result.stdout.encode("utf-8"))


def create_app_with_args(args: List[str]):
    """Create a Platypus app using the CLT."""
    cmd = [
        str(CLT_BINARY),
        *args,
        "--overwrite",
        "--executable-path",
        str(SCRIPTEXEC_BINARY),
        "--nib-path",
        str(NIB_PATH),
        "--name",
        TEST_APP_NAME,
        str(ARGS_SCRIPT_PATH),
        str(TEST_APP_PATH),
    ]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True, capture_output=True)


def test_default_profile_sanity():
    """Check the basic sanity of the default profile."""
    plist = get_profile_plist_for_args([])
    assert plist["Version"] == "1.0"
    assert plist["InterpreterPath"] == "/bin/sh"
    assert plist["InterfaceType"] == "Text Window"
    assert len(plist["BundledFiles"]) == 0
    assert not plist["Authentication"]
    assert plist["Name"] != ""
    assert re.match(r"\w+\.\w+\.\w+", plist["Identifier"])


def test_profile_generation_boolean_switches():
    """Test profile generation with boolean switches."""
    boolean_opts = {
        "-A": "Authentication",
        "-D": ["Droppable", "AcceptsFiles"],
        "-F": "AcceptsText",
        "-N": "DeclareService",
        "-B": "RunInBackground",
        "-Z": "PromptForFileOnLaunch",
        "-c": "StatusItemUseSystemFont",
        "-d": "DevelopmentVersion",
        "-l": "OptimizeApplication",
        "-y": "Overwrite",
    }

    for flag, key in boolean_opts.items():
        plist = get_profile_plist_for_args([flag])
        keys_to_check = key if isinstance(key, list) else [key]
        for k in keys_to_check:
            assert plist[k] is True, f"Flag {flag} should set {k} to True"

    # Test inverted boolean
    plist = get_profile_plist_for_args(["-R"])
    assert plist["RemainRunning"] is False, "Flag -R should set RemainRunning to False"


def test_profile_generation_string_options():
    """Test profile generation with string-based options."""
    string_opts = {
        "-a": ("Name", "MyAppName"),
        "-o": ("InterfaceType", "Progress Bar"),
        "-p": ("InterpreterPath", "/usr/bin/perl"),
        "-V": ("Version", "3.2"),
        "-u": ("Author", "Alan Smithee"),
        "-I": ("Identifier", "org.something.Blergh"),
        "-b": ("TextBackground", "#000000"),
        "-g": ("TextForeground", "#ffeeee"),
        "-K": ("StatusItemDisplayType", "Icon"),
        "-Y": ("StatusItemTitle", "MySillyTitle"),
    }

    for flag, (key, value) in string_opts.items():
        plist = get_profile_plist_for_args([flag, value])
        assert plist[key] == value, f"Flag {flag} should set {key} to {value}"


def test_profile_generation_data_options():
    """Test profile generation with options that take file paths (data)."""
    data_opts = {
        "-i": ("IconPath", DUMMY_ICON_PATH),
        "-Q": ("DocIconPath", DUMMY_ICON_PATH),
        "-L": ("StatusItemIcon", DUMMY_ICON_PATH),
    }
    for flag, (key, value) in data_opts.items():
        plist = get_profile_plist_for_args([flag, str(value)])
        assert plist[key] is not None, f"Flag {flag} should set {key}"


def test_profile_generation_multiple_arg_options():
    """Test profile generation for flags that accept multiple arguments."""
    dummy1_path = Path("dummy1").resolve()
    dummy2_path = Path("dummy2").resolve()

    multiple_items_opts: Dict[str, Union[str, List[Any]]] = {
        "-G": ["InterpreterArgs", ["-a", "-b", "-c"]],
        "-C": ["ScriptArgs", ["-e", "-f", "-g"]],
        "-f": ["BundledFiles", [str(dummy1_path), str(dummy2_path)]],
        "-X": ["Suffixes", ["txt", "png", "pdf"]],
        "-T": ["UniformTypes", ["public.text", "public.rtf"]],
        "-U": ["URISchemes", ["https", "ssh"]],
    }

    for flag, (key, values) in multiple_items_opts.items():
        plist = get_profile_plist_for_args([flag, "|".join(values)])
        assert all(item in plist[key] for item in values)


def test_app_directory_structure_and_permissions():
    """Verify the app bundle's directory structure and permissions."""
    create_app_with_args(["-R"])

    base_path = TEST_APP_PATH
    paths_to_check = [
        base_path,
        base_path / "Contents",
        base_path / "Contents/Info.plist",
        base_path / "Contents/MacOS",
        base_path / "Contents/MacOS" / TEST_APP_NAME,
        base_path / "Contents/Resources",
        base_path / "Contents/Resources/AppSettings.plist",
        base_path / "Contents/Resources/MainMenu.nib",
        base_path / "Contents/Resources/script",
    ]

    for path in paths_to_check:
        assert path.exists(), f"Path does not exist: {path}"

    app_binary = base_path / "Contents/MacOS" / TEST_APP_NAME
    script = base_path / "Contents/Resources/script"

    assert os.access(app_binary, os.X_OK), "App binary should be executable"
    assert os.access(script, os.X_OK), "Bundled script should be executable"


@pytest.mark.gui
def test_app_argument_handling():
    """
    Verify that the created app correctly handles command-line arguments.
    This is a GUI test and will be skipped unless --run-gui is specified.
    """
    create_app_with_args(["-R"])

    app_executable = TEST_APP_PATH / "Contents/MacOS" / TEST_APP_NAME
    args_to_test = ["foo", "bar", "baz"]

    subprocess.run([str(app_executable), *args_to_test], check=True)

    assert ARGS_OUT_FILE.exists()
    with open(ARGS_OUT_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        assert lines == args_to_test
