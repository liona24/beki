#!/bin/bash

set -e

DIST=dist
BUNDLE="$DIST/bundle"
APP="$BUNDLE/app"
TEX="$BUNDLE/tex"

rm -rf "$BUNDLE"

mkdir -p "$APP"
mkdir -p "$TEX"

echo "Collecting backend .."
find backend/ -name '*.py' -not -name 'settings.py' -type f -exec bash -c "echo '{}' && cp {} $APP/\$(basename {})" \;

echo "Collecting TeX files .."
find tex/ -type f -exec bash -c "echo '{}' && cp {} $TEX/\$(basename {})" \;

echo "Building frontend .."
pushd beki/
yarn install
yarn build
popd
