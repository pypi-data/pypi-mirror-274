#!/bin/bash

# Get the directory of the currently executing script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set the PYTHONPATH to include the script directory
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}"

# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python src/html_writer.py

bash chmod +x run.sh
