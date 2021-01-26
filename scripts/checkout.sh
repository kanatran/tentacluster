#!/bin/bash

echo Checking out to $1
cd ../baquap
pwd
git checkout --orphan $1
rm -rf README.md

exit 0