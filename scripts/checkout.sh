#!/bin/bash

echo Checking out to $1
cd ../baquap
pwd
git checkout -b $1
git checkout $1
rm -rf README.md

exit 0