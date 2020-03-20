#!/bin/bash

# Initialize the variables
INPUT_FILE=$1
OUTPUT_FILE=$2
CURRENT_DIR=$(dirname $0)

# Call the python script
echo "Calling process_federal_complaints.py script with provided args"
${CURRENT_DIR}/src/process_federal_complaints.py ${INPUT_FILE} ${OUTPUT_FILE}
