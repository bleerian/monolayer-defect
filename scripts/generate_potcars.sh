#!/bin/bash

# Check if POTCAR environment variable is set
if [ -z "$POTCAR" ]; then
    echo "Error: The POTCAR environment variable is not set!"
    exit 1
fi

# Prompt user for number of elements
read -p "Enter the number of elements: " num_elements

# Initialize empty POTCAR content
> POTCAR

# Prompt user for each element and concatenate the POTCAR files
for (( i=1; i<=$num_elements; i++ )); do
    read -p "Enter element $i: " element
    cat "$POTCAR/$element/POTCAR" >> POTCAR
done

echo "POTCAR generated successfully!"


