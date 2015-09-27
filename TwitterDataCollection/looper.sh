#!/bin/bash
while :
do
  python TwitterCrawler.py
  for ((i = 0; i < 60; i++))
  do
    echo $i
    sleep 1
  done
done
