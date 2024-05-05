#!/bin/sh
export build_count=100000
./generate.py --builds $build_count --input-file ../dict/social.tsv --output-file social-1.xd
rm social-1.xd-guesses.json1
./generate.py --builds $build_count --input-file ../dict/business.tsv --output-file business-1.xd
rm business-1.xd-guesses.json1
./generate.py --builds $build_count --input-file ../dict/travel.tsv --output-file travel-1.xd
rm travel-1.xd-guesses.json1
./generate.py --builds $build_count --input-file ../dict/food.tsv --output-file food-1.xd
rm food-1.xd-guesses.json1
