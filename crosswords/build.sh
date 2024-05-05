#!/bin/sh
export build_count=100000
./generate.py --builds $build_count --must-connect --favour-words --input-file ../dict/social.tsv --output-file social-1.xd
rm social-1.xd-guesses.json1
./generate.py --builds $build_count --must-connect --input-file ../dict/social.tsv --output-file social-2.xd
rm social-2.xd-guesses.json1
./generate.py --builds $build_count --must-connect --favour-words --input-file ../dict/business.tsv --output-file business-1.xd
rm business-1.xd-guesses.json1
./generate.py --builds $build_count --must-connect --input-file ../dict/business.tsv --output-file business-2.xd
rm business-2.xd-guesses.json1
./generate.py --builds $build_count --must-connect --favour-words --input-file ../dict/travel.tsv --output-file travel-1.xd
rm travel-1.xd-guesses.json1
./generate.py --builds $build_count --must-connect --input-file ../dict/travel.tsv --output-file travel-2.xd
rm travel-2.xd-guesses.json1
./generate.py --builds $build_count --must-connect --favour-words --input-file ../dict/food.tsv --output-file food-1.xd
rm food-1.xd-guesses.json1
./generate.py --builds $build_count --must-connect --input-file ../dict/food.tsv --output-file food-2.xd
rm food-2.xd-guesses.json1
