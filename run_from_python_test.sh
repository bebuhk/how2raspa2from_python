#!/bin/bash

# Check if exactly three arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <number1> <number2> <number3>"
    echo "did not get 3 arguments" >&2 # to stderr
    exit 1
fi

# Assign input arguments to variables
number1=$1
number2=$2
number3=$3

# Print the numbers
echo "Number 1: $number1"
echo "Number 2: $number2"
echo "Number 3: $number3"