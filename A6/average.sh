#!/bin/bash

# Specify the input file path or name
input_file="output.txt"

# Initialize associative array to store player data
declare -A player_gold
declare -A player_count

# Read the input file line by line
while IFS= read -r line
do
  # Check if the line contains the desired pattern
  if [[ $line == "Player"*"Health"*"Gold"*"Position" ]]; then
    # Read the following lines until the "Gold pots:" line is encountered
    while IFS= read -r data_line
    do
      # Check if the line contains the end of the table marker
      if [[ $data_line == "Gold Pots:" ]]; then
        break
      fi

      # Extract the values from the data line
      player=$(echo "$data_line" | awk '{print $1}')
      gold=$(echo "$data_line" | awk '{print $3}')

      # Accumulate the values for each player
      player_gold[$player]=$(( player_gold[$player] + gold ))
      player_count[$player]=$(( player_count[$player] + 1 ))
    done
  fi
done < "$input_file"

# Calculate averages for each player
echo "Average Gold per Player:"
for player in "${!player_gold[@]}"
do
  average_gold=$(( player_gold[$player] / player_count[$player] ))
  echo "Player $player: $average_gold"
done

