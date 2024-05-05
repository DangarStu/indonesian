#!/bin/sh
./generate.py --builds 200000 --must-connect --input-file ../dict/social.tsv --output-file social.xd
rm social.xd-guesses.json1
./generate.py --builds 200000 --must-connect --input-file ../dict/business.tsv --output-file business.xd
rm business.xd-guesses.json1
./generate.py --builds 200000 --must-connect --input-file ../dict/travel.tsv --output-file travel.xd
rm travel.xd-guesses.json1
./generate.py --builds 200000 --must-connect --input-file ../dict/food.tsv --output-file food.xd
rm food.xd-guesses.json1
