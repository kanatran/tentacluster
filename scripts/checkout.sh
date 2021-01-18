#!/bin/bash

echo Checking out to $1
cd ../baquap
pwd
git checkout -b $1
git checkout $1

exit 0