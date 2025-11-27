#!/usr/bin/env python3
"""A simple script that writes its command-line arguments to a file.
This script is intended to be bundled into a Platypus application for testing
argument passing."""

import sys
import os
from pathlib import Path

# The ScriptExec process sets the CWD to the app's Resources folder.
# The test expects the output file in the directory where the test is run,
# which is three levels up from the Resources folder.
OUTPUT_FILE = Path("../../../args.txt")

def main():
    """Write command-line arguments to the output file."""
    # Ensure the file is cleared before writing
    try:
        OUTPUT_FILE.unlink()
    except FileNotFoundError:
        pass

    # Write all arguments (excluding the script name) to the file, one per line.
    with open(OUTPUT_FILE, "w") as f:
        for arg in sys.argv[1:]:
            f.write(arg + "\n")

if __name__ == "__main__":
    main()

