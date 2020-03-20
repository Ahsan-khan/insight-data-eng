#!/bin/bash

# Initialize the variables
CURRENT_DIR=$(dirname $0)

# Call the python script
echo "Calling process_federal_complaints.py script with provided args"
python3 ${CURRENT_DIR}/src/process_federal_complaints.py ${CURRENT_DIR}/input/complaints.csv ${CURRENT_DIR}/output/report.csv
