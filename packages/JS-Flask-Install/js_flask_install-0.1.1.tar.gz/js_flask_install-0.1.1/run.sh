#!/bin/bash

# Get the directory of the currently executing script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set the PYTHONPATH to include the script directory
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}"

# Activate the virtual environment
source env/bin/activate

# Run the Python script
python src/writefile_js.py

# Deactivate the virtual environment
deactivate
