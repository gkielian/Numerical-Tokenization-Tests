#!/bin/bash

for file in ./data/2016.NBA.Raw.SportVU.Game.Logs/*/*.json; do
  echo "$file"
  python3 main.py --path "$file"
done

