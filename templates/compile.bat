#!/usr/bin/env bash
set -ex
new="$1"
new="$(echo "$new" | sed -E 's/\/$//')"
cd "$new"
./gradlew assembleDebug

