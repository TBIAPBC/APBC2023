#!/bin/bash

# Loop 100 times
for ((i=1; i<=200; i++))
do
  # Execute the command and capture the output
  output=$(python runRobotRace.py --number 100)

  # Extract the desired part of the output and store it in a text file
  desired_output=$(echo "$output" | awk '/Final board:/{flag=1; next} flag')
  echo "$desired_output" >> output.txt
done


