#!/bin/bash

echo Committing to $1
pushd ../../../baquap
git add .
git commit --amend -m "Updated transcripts"
git commit -m "Created transcripts"
git push --set-upstream origin testvideo -f

exit 0