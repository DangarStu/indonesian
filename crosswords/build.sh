#!/bin/sh
./generate.py --builds 50000 --must-connect --favour-words --input-file ../dict/social.tsv --output-file social-1.xd
./generate.py --builds 50000 --must-connect --input-file ../dict/social.tsv --output-file social-2.xd
rm social.xd-guesses.json1
./generate.py --builds 50000 --must-connect --favour_words --input-file ../dict/business.tsv --output-file business-1.xd
./generate.py --builds 50000 --must-connect --input-file ../dict/business.tsv --output-file business-2.xd
rm business.xd-guesses.json1
./generate.py --builds 50000 --must-connect --favour_words --input-file ../dict/travel.tsv --output-file travel-1.xd
./generate.py --builds 50000 --must-connect --input-file ../dict/travel.tsv --output-file travel-2.xd
rm travel.xd-guesses.json1
./generate.py --builds 50000 --must-connect --favour_words --input-file ../dict/food.tsv --output-file food-1.xd
./generate.py --builds 50000 --must-connect --input-file ../dict/food.tsv --output-file food-2.xd
rm food.xd-guesses.json1
